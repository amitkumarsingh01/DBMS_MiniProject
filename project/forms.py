from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, DateTimeField, FileField, HiddenField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('user', 'User'), ('admin', 'Admin'), ('staff', 'Staff')], validators=[DataRequired()])

class QueryForm(FlaskForm):
    department = SelectField('Department', choices=[('1', 'Department 1'), ('2', 'Department 2'), ('3', 'Department 3'), ('4', 'Department 4')], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    date = DateTimeField('Date', validators=[DataRequired()])
    suggestion = TextAreaField('Suggestion')
    image = FileField('Image/Video')
    geolocation = StringField('Geolocation')

class FeedbackForm(FlaskForm):
    query_id = HiddenField('Query ID', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired()])
    suggestion = TextAreaField('Suggestion')
