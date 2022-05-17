from flask import Flask, render_template, request, flash, redirect, url_for, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import logout_user, login_user, LoginManager, current_user, login_required
from forms import LoginForm, RegistrationForm, DiaryForm, EntryForm
import models
from is_safe_url import is_safe_url
from contextlib import contextmanager


app = Flask(__name__)

app.config['SECRET_KEY'] = 'Ligmaballz!!!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))

#@app.context_processor
#def context_processor():
    #return title == "My awesome website"
#    pass

@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')

@app.route('/diary', methods=['GET', 'POST'])
@login_required
def diary():
    diary = models.Diary.query.filter_by(user_id=current_user.id).all()
    return render_template('diary_index.html', diary=diary)

@app.route('/diary/<string:diary_id>')
@login_required
def open_diary(id):
    if request.method =="POST":
        form = EntryForm()
        id = request.form['id']
        diary = models.Diary.query.filter_by(id=id).all()
    return jsonify({'htmlresponse': render_template('open_diary.html', form=form)})

@app.route('/create_diary', methods=['POST'])
@login_required
def create_diary():
    if request.method == "POST":
        form = DiaryForm()
        if form.validate_on_submit():
            create_diary = models.Diary(user_id=current_user, title=form.title.data)
            print(diary)
            db.session.add(diary)
            db.session.commit()
            return redirect(url_for('diary'))
    return jsonify({'htmlresponse': render_template('create_diary.html', form=form)})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('wrong password or username')
        else:
            login_user(user, remember=form.remember_me.data)
            flash('Logged in successfully.')
        next = request.args.get('next')
        if not is_safe_url(next, allowed_hosts="localhost:5000"):
            return abort(400)
        return redirect(next or url_for('index'))
    return render_template('login.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = models.User(email=form.email.data, username=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now a registered user.')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
