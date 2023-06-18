from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from mainpro.models import User

class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=2, max=20),
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
        ]
    )
    conf_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )
    first_name = StringField(
        'First name',
        validators=[
            DataRequired(),
        ]
    )
    last_name = StringField(
        'Last name',
        validators=[
            DataRequired(),
        ]
    )
    middle_name = StringField(
        'Middle name',
        validators=[
            DataRequired(),
        ]
    )
    birth_date = DateField(
        'Birthdate',
        validators=[
            DataRequired(),
        ]
    )
    submit = SubmitField(
        'Sign Up'
    )

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username is taken, try another one.")

            
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email is already registered, you can't register with one email more than once.")



class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
        ]
    )

    submit = SubmitField(
        'Login'
    )