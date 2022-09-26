from flask import (Flask, render_template, request, flash,
                   redirect, url_for, abort, jsonify)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (logout_user, login_user, LoginManager,
                         current_user, login_required)
from forms import (LoginForm, RegistrationForm, DiaryForm, EntryForm,
                   AddTagForm, DeletionForm)
import models
from contextlib import contextmanager
from datetime import datetime
from flask_ckeditor import CKEditor

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Ligmaballz!!!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app, session_options={'autoflush': False})
login_manager = LoginManager()
login_manager.init_app(app)

# text editor for entry page
ckeditor = CKEditor(app)


# flask login manager
@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login'))


# route for index
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')

# route that displays all of the user's diaries
@app.route('/diary', methods=['GET', 'POST'])
@login_required
def diary_index():
    diary = models.Diary.query.filter_by(user_id=current_user.id).all()
    return render_template('diary_index.html', diary=diary)


# route that displays entries of specific diary
@app.route('/diary/<int:id>', methods=['GET', 'POST'])
@login_required
def diary(id):
    diary = models.Diary.query.filter_by(user_id=current_user.id, id=id).all()
    if len(diary) == 0:
        abort(404)
    return render_template('diary.html', diary=diary)


# route that creates a new diary for the user
@app.route('/diary/create', methods=['GET', 'POST'])
@login_required
def create_diary():
    form = DiaryForm()
    if form.validate_on_submit():
        # query to add data to diary table
        diary = models.Diary(user_id=current_user.id, title=form.title.data)
        db.session.add(diary)
        db.session.commit()
        flash(f'Created new diary: "{diary.title}"')
        return redirect(url_for('diary_index'))
    return render_template('create_diary.html', form=form)


# route that edits an existing diary
@app.route('/diary/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_diary(id):
    form = DiaryForm()
    diary = models.Diary.query.filter_by(user_id=current_user.id,
                                         id=id).first_or_404()
    if form.validate_on_submit():
        # edit existing row in database
        diary.title = form.title.data
        db.session.merge(diary)
        db.session.commit()
        flash(f'Diary title has been changed to: "{diary.title}"')
        return redirect(url_for('diary', id=diary.id))
    form.title.data = diary.title
    return render_template('edit_diary.html', form=form, diary=diary)


# route that deletes a user's diary
@app.route('/diary/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_diary(id):
    diary = models.Diary.query.filter_by(user_id=current_user.id,
                                         id=id).first_or_404()
    form = DeletionForm()
    if form.validate_on_submit():
        # deletes diary object
        local = db.session.merge(diary)
        db.session.delete(local)
        db.session.commit()
        flash(f'Diary: "{diary.title}" was deleted')
        return redirect(url_for('diary_index'))
    return render_template('delete_diary.html', form=form, diary=diary)


# route that displays user entries and allows editing of notes
@app.route('/entry/<int:id>', methods=['GET', 'POST'])
@login_required
def entry(id):
    form = EntryForm()
    entry = models.Entry.query.filter_by(user_id=current_user.id,
                                         id=id).first_or_404()
    if form.validate_on_submit():
        entry.notes = form.notes.data
        db.session.merge(entry)
        db.session.commit()
        flash('Saved notes')
        return redirect(url_for('entry', id=id))
    form.notes.data = entry.notes
    return render_template('entry.html', entry=entry, form=form)


# route that allows user to create a new entry in the diary
@app.route('/entry/create/<int:id>', methods=['GET', 'POST'])
@login_required
def create_entry(id):
    entry = models.Entry.query.filter_by(user_id=current_user.id, diary_id=id,
                                         date=datetime.today().date()).first()
    date = entry.date.strftime('%B %d, %Y')
    if entry is None:
        entry = models.Entry(user_id=current_user.id, diary_id=id,
                             date=datetime.today().date())
        db.session.add(entry)
        db.session.commit()
        flash(f'Created new entry for "{date}"')
    flash(f'redirected to existing entry for {date}')
    return redirect(url_for('entry', id=entry.id))


# route that allows user to delete an entry
@app.route('/entry/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_entry(id):
    entry = models.Entry.query.filter_by(user_id=current_user.id,
                                         id=id).first_or_404()
    form = DeletionForm()
    if form.validate_on_submit():
        date = entry.date.strftime('%B %d, %Y')
        local = db.session.merge(entry)
        db.session.delete(local)
        db.session.commit()
        flash(f'Deleted entry for "{date}"')
        return redirect(url_for('diary', id=entry.diary.id))
    return render_template('delete_entry.html', form=form, entry=entry)


# route that allows the user to add tags to an entry
@app.route('/entry/<int:id>/tag/add/', methods=['GET', 'POST'])
@login_required
def add_tag(id):
    form = AddTagForm()
    if form.validate_on_submit():
        # formatting the tag
        name = form.name.data.lower().strip()
        tag = models.Tag.query.filter_by(user_id=current_user.id,
                                         name=name).first()
        entry = models.Entry.query.filter_by(user_id=current_user.id,
                                             id=id).first_or_404()
        # checking if the user has already created this tag
        if tag is None:
            # creating a tag
            tag_to_add = models.Tag(user_id=current_user.id, name=name)
            local = db.session.merge(tag_to_add)
            db.session.add(local)
            db.session.commit()
        # adding to the association table
        tag = models.Tag.query.filter_by(user_id=current_user.id,
                                         name=name).first_or_404()
        entry.tags.append(tag)
        db.session.merge(entry)
        db.session.commit()
        flash(f'added tag: "{name}"')
        return redirect(url_for('entry', id=entry.id))
    return render_template('create_tag.html', form=form)


# dissociate a tag from an entry
@app.route('/entry/<int:id>/tag/remove/<int:tid>', methods=['GET', 'POST'])
@login_required
def remove_tag(id, tid):
    entry = models.Entry.query.filter_by(user_id=current_user.id,
                                         id=id).first_or_404()
    tag = models.Tag.query.filter_by(user_id=current_user.id,
                                     id=tid).first_or_404()
    # removing from the association table
    entry.tags.remove(tag)
    db.session.merge(entry)
    db.session.commit()
    flash(f'removed tag: "{tag.name}"')
    return redirect(url_for('entry', id=entry.id))


# route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # sends back to diary list if already logged in
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        # if user doesn't exist or if password is incorrect it tells them
        if user is None or not user.check_password(form.password.data):
            flash('wrong password or email')
        else:
            # login user if user information is correct
            login_user(user, remember=form.remember_me.data)
            flash('Logged in successfully.')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


# route for register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        # if it already exists it tells them
        if user is not None:
            flash('User already exists')
        else:
            # puts email, and password into the database
            user = models.User(email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
            flash('You are now a registered user.')
    return render_template('register.html', form=form)


# route for logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out.')
    return redirect(url_for('login'))


# error handler for a 404 error (returns 404.html instead of standard 404 page)
@app.errorhandler(404)
def error404(error):
    return render_template('404.html', title='Error'), 404


# error handler for a 500 error (returns 500.html instead of standard 500 page)
@app.errorhandler(500)
def error500(error):
    return render_template('500.html')


# error handler for a 401 error (returns 401.html instead of standard 401 page)
@app.errorhandler(401)
def error401(error):
    return render_template('401.html')


if __name__ == '__main__':
    app.run(debug=True)
