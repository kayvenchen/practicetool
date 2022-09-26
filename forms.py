from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Length
from wtforms.fields import DateField
from flask_ckeditor import CKEditorField


# defines variables in LoginForm
class LoginForm(FlaskForm):
    email = StringField('Username', validators=[DataRequired(), Length(max=256)], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired(), Length(max=36)], render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


# defines variables in RegistrationForm
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=256)], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired(), Length(max=36)], render_kw={"placeholder": "Password"})
    # makes sure 2nd password is same as 1st password
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password'), Length(max=36)], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Register')


# defines variables in DiaryForm
class DiaryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=36)], render_kw={"placeholder": "Title"})
    submit = SubmitField('Save')

# defines variables in EntryForm
class CreateEntryForm(FlaskForm):
    notes = DateField('Notes', validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField('Save')

# defines variables in EntryForm
class EntryForm(FlaskForm):
    notes = CKEditorField('Notes', validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField('Save')

# defines variables in AddTagForm
class AddTagForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(max=36)], render_kw={"placeholder": "Tag"})
    submit = SubmitField('Save')

# defines variables in AddTagForm
class DeletionForm(FlaskForm):
    submit = SubmitField('Delete')
