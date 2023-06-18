from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, DateField, FileField, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from mainpro.models import User
import re
from flask_login import current_user

class RegistrationForm(FlaskForm):

    first_name = StringField(
        "First Name",
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
    )

    middle_name = StringField(
        "Middle Name",
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
    )

    last_name = StringField(
        "Last Name",
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
    )

    birth_date = DateField(
        'Birth Date',
        format='%Y-%m-%d',
        validators=[
            DataRequired()
        ]
    )

    profile_image = FileField(
        'Profile Image', 
        validators=[
            FileAllowed(['jpeg', 'jpg', 'png'], 'only images are allowed' ), 
            FileRequired('File Field shoud not be empty')]
    )

    current_profile_image = HiddenField('Current Profile Image')


    username = StringField(
        "User Name",
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ]
    )

    submit = SubmitField(
        "Sign Up"
    )

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("User Name is already exist")
    
    def validate_email(self,email):
        emaill = User.query.filter_by(email=email.data).first()
        if emaill:
            raise ValidationError("Email is already exist")

class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Log In")

    def validate_email(self,email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        email = email.data
        if not re.match(pattern, email):
            raise ValidationError("Invalid Email")


class PostForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
        )

    content = TextAreaField(
        'Post Content',
        validators=[
            DataRequired()
        ]
        )

    status = SelectField(u'Share with', 
                        choices=[('Public', 'Public'), ('Friends_only', 'Friends_only'), ('Only_me', 'Only_me')]
        )

    
    post_image= FileField(
        'Image'
    )
    
    submit = SubmitField(
        'Save Post'
    )
    
class EditForm(FlaskForm):

    first_name = StringField(
        "First Name",
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
    )

    middle_name = StringField(
        "Middle Name",
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
    )

    last_name = StringField(
        "Last Name",
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
    )

    birth_date = DateField(
        'Birth Date',
        format='%Y-%m-%d',
        validators=[
            DataRequired()
        ]
    )

    profile_image = FileField(
        'Profile Image', 
        validators=[
            FileAllowed(['jpeg', 'jpg', 'png'], 'only images are allowed' ), 
            FileRequired('File Field shoud not be empty')]
    )

    current_profile_image = HiddenField('Current Profile Image')


    username = StringField(
        "User Name",
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )



    submit = SubmitField(
        "Save Changes"
    )

    def validate_username(self,username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("User Name is already exist")
        
    def validate_email(self,email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("User Name is already exist")

