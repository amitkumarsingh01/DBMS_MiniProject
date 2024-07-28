from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DateField, FileField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.fields import EmailField

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    role = SelectField('Role', choices=[('user', 'User'), ('staff', 'Staff'), ('admin', 'Admin')], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class QueryForm(FlaskForm):
    department = SelectField('Department', choices=[('1', 'Department 1'), ('2', 'Department 2'), ('3', 'Department 3'), ('4', 'Department 4')], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    suggestion = TextAreaField('Suggestion')
    image_file = FileField('Upload Image/Video')
    geolocation = StringField('Geolocation')
    submit = SubmitField('Submit')

class FeedbackForm(FlaskForm):
    rating = SelectField('Rating', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    suggestion = TextAreaField('Suggestion')
    submit = SubmitField('Submit')
