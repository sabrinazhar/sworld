" forms.py file that contains all the forms"

from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, validators, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from app.models import User

# Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])

# SignUp Form
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[
        validators.DataRequired(),
        validators.Length(max=32,
                          message='Username must be at most 32 characters.')
    ])
    password = PasswordField('Password', validators=[
        validators.DataRequired(),
        validators.Length(min=12,
                          message='Password must be at least 12 characters.'),
        validators.Regexp(
            regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).*$",
            message='Password must contain at least an uppercase letter, a lowercase letter, a digit.'
        )
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        validators.DataRequired(),
        validators.EqualTo('password',
                           message='Passwords does not match. Try again.')
    ])
    submit = SubmitField('Sign Up')

# Edit Username Form
class EditUsernameForm(FlaskForm):
    new_username = StringField('New Username', validators=[
        DataRequired(),
        Length(max=32)
    ])
    submit = SubmitField('Save Changes')

    def validate_new_username(self, field):
        # Check if the new username already exists
        existing_user = User.query.filter_by(username=field.data).first()
        if existing_user:
            raise ValidationError('Username already exists. Please choose a different username.')

# Edit Password Form
class EditPasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[
        validators.DataRequired(),
        validators.Length(min=12,
                          message='Password must be at least 12 characters.'),
        validators.Regexp(
            regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).*$",
            message='Password must contain at least an uppercase letter, a lowercase letter, and a digit.'
        )
    ])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        validators.DataRequired(),
        validators.EqualTo('new_password',
                           message='Passwords do not match. Try again.')
    ])
    submit = SubmitField('Update Password')

class EditFontSizeForm(FlaskForm):
    font_size_choices = [('normal', 'Normal'), ('small', 'Small'),
                         ('large', 'Large')]
    font_size = SelectField('Font Size',
                            choices=font_size_choices,
                            validators=[DataRequired()])
    submit = SubmitField('Save Changes')

class SearchForm(FlaskForm):
    username = StringField('Username', validators=[validators.Length(max=32)])
    submit = SubmitField(' ')
