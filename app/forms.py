from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EditMemberForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    birthdate = DateField('Birthdate', format='%Y-%m-%d', validators=[DataRequired()])  # Change to DateField
    relationship = StringField('Relationship', validators=[DataRequired(), Length(max=100)])
    address = StringField('Address', validators=[Length(max=200)])
    medical_records = TextAreaField('Medical Records', validators=[Length(max=500)])
    notes = TextAreaField('Notes', validators=[Length(max=500)])
    submit = SubmitField('Save Changes')
