from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired



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
    
