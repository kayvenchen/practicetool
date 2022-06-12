from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, StringField, TextAreaField, FileField, DateField, TimeField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Length
from wtforms.fields.html5 import DateField, TimeField


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=256)], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired(), Length(max=36)], render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=256)], render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=256)], render_kw={"placeholder": "email"})
    password = PasswordField('Password', validators=[DataRequired(), Length(max=36)], render_kw={"placeholder": "Password"})
    # makes sure 2nd password is same as 1st password
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password'), Length(max=36)], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Register')

class DiaryForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()], render_kw={"placeholder": "Title"})
    submit = SubmitField('Create')

class EntryForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()], render_kw={"placeholder": "Title"})
    date = DateField("Date", format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField("Start Time", validators=[DataRequired()])
    end_time = TimeField("End Time", validators=[DataRequired()])
    notes = TextAreaField("Notes", validators=[DataRequired()], render_kw={"placeholder": "notes"})
    submit = SubmitField('Enter')


class ImageForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    file = FileField("File", validators=[DataRequired()])
