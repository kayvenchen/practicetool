from flask import Flask, render_template, request, flash, redirect, url_for, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import logout_user, login_user, LoginManager, current_user, login_required
from forms import LoginForm, RegistrationForm, DiaryForm, EntryForm
import models
from contextlib import contextmanager
from datetime import datetime
from flask_ckeditor import CKEditor

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Ligmaballz!!!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

ckeditor = CKEditor(app)

@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login'))

#@app.context_processor
#def context_processor():
    #return title == "My awesome website"
#    passi

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    diary = models.Diary.query.filter_by(user_id=current_user.id).all()
    return render_template('diary_index.html', diary=diary)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = DiaryForm()
    if form.validate_on_submit():
        diary = models.Diary(user_id=current_user.id, title=form.title.data)
        db.session.add(diary)
        db.session.commit()
        flash('Created new Diary')
        return redirect(url_for('index'))
    return render_template('create_diary.html', form=form)

@app.route('/diary/<int:id>', methods=['GET', 'POST'])
@login_required
def diary(id):
    diary = models.Diary.query.filter_by(user_id=current_user.id, id=id).all()
    return render_template('diary.html', diary=diary)

@app.route('/entry/<int:id>', methods=['GET', 'POST'])
@login_required
def entry(id):
    entry = models.Entry.query.filter_by(user_id=current_user.id, id=id).first()
    return render_template('entry.html', entry=entry)

@app.route('/edit_entry/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_entry(id):
    form = EntryForm()
    entry = models.Entry.query.filter_by(user_id=current_user.id, id=id).first()
    form.notes.data = entry.notes
    if form.validate_on_submit():
        new_entry = models.Entry(user_id=current_user.id, id=id notes=form.notes.data)
        db.session.update(new_entry)
        db.session.commit()
    return render_template('open_diary.html', form=form, entry=entry)

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
        return redirect(url_for('index'))
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
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
