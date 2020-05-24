"""This is the forms module.

Provides LoginForm class for app.
"""
from bakalarka.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError






class LoginForm(FlaskForm):
    """LoginForm model.

    Attributes:
        email (StringField): Email input.
        password (PasswordField): Password input.
        remember (BooleanField): Remember me checkbox.
        submit (SubmitField): Submit button.
    """
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
