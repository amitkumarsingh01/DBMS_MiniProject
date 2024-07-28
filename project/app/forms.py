from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, IntegerField, FileField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class QueryForm(FlaskForm):
    department = SelectField('Department', choices=[('1', 'Dept 1'), ('2', 'Dept 2'), ('3', 'Dept 3'), ('4', 'Dept 4')], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    suggestion = TextAreaField('Suggestion')
    image_file = FileField('Upload Image/Video')
    geolocation = StringField('Geolocation')
    submit = SubmitField('Submit')

class FeedbackForm(FlaskForm):
    rating = IntegerField('Rating of Satisfaction', validators=[DataRequired()])
    suggestion = TextAreaField('Suggestion')
    submit = SubmitField('Submit')
