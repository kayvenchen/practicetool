from flask import Flask, render_template, request, flash, redirect, url_for, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import logout_user, login_user, LoginManager, current_user, login_required
from forms import LoginForm, RegistrationForm, DiaryForm, EntryForm, AddTagForm
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
#    pass

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    diary = models.Diary.query.filter_by(user_id=current_user.id).all()
    return render_template('diary_index.html', diary=diary)


@app.route('/diary/<int:id>', methods=['GET', 'POST'])
@login_required
def diary(id):
    diary = models.Diary.query.filter_by(user_id=current_user.id, id=id).all()
    return render_template('diary.html', diary=diary)


@app.route('/diary/create', methods=['GET', 'POST'])
@login_required
def create_diary():
    form = DiaryForm()
    if form.validate_on_submit():
        diary = models.Diary(user_id=current_user.id, title=form.title.data)
        db.session.add(diary)
        db.session.commit()
        flash('Created new Diary')
        return redirect(url_for('index'))
    return render_template('create_diary.html', form=form)


@app.route('/diary/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_diary(id):
    form = DiaryForm()
    diary = models.Diary.query.filter_by(user_id=current_user.id, id=id).first_or_404()
    if form.validate_on_submit():
        diary.title = form.title.data
        db.session.merge(diary)
        db.session.commit()
        flash('edited new diary name')
        return redirect(url_for('diary', id=diary.id))
    return render_template('create_diary.html', form=form)


@app.route('/diary/delete/<int:id>')
def delete_diary(id):
    diary = models.Diary.query.filter_by(user_id=current_user.id, id=id).first()
    local = db.session.merge(diary)
    db.session.delete(local)
    db.session.commit()
    #return a message
    flash("entry post was deleted")
    return redirect(url_for('index'))


@app.route('/entry/<int:id>', methods=['GET', 'POST'])
@login_required
def entry(id):
    form = EntryForm()
    entry = models.Entry.query.filter_by(user_id=current_user.id, id=id).first_or_404()
    if form.validate_on_submit():
        entry.notes = form.notes.data
        db.session.merge(entry)
        db.session.commit()
    form.notes.data = entry.notes
    return render_template('entry.html', entry=entry, form=form)

@app.route('/entry/create/<int:id>', methods=['GET', 'POST'])
@login_required
def create_entry(id):
    entry = models.Entry(user_id=current_user.id, diary_id=id)
    db.session.add(entry)
    db.session.commit()
    return redirect(url_for('entry', id=entry.id))

@app.route('/entry/delete/<int:id>')
def delete_entry(id):
    entry = models.Entry.query.filter_by(user_id=current_user.id, id=id).first_or_404()
    local = db.session.merge(entry)
    db.session.delete(local)
    db.session.commit()
    return redirect(url_for('diary', id=entry.diary.id))

@app.route('/entry/<int:id>/tag/add/', methods=['GET', 'POST'])
@login_required
def add_tag(id):
    form = AddTagForm()
    if form.validate_on_submit():
        name = form.name.data.lower().strip()
        tag = models.Tag.query.filter_by(user_id=current_user.id, name=name).first()
        entry = models.Entry(user_id=current_user.id, id=id)
        print(entry)
        if tag is None:
            tag_to_add = models.Tag(user_id=current_user.id, name=name)
            local = db.session.merge(tag_to_add)
            db.session.add(local)
            print(tag_to_add)
            db.session.commit()
        entry.tags.append(tag)
        db.session.merge(entry)
        db.session.commit()
        return redirect(url_for('entry', id=entry.id))

    return render_template('create_tag.html', form=form)

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
        db.session.merge(user)
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
