from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField, Form
from wtforms.fields.html5 import EmailField
from wtforms.validators import data_required, Length,Email,EqualTo

class LoginForm(FlaskForm):
    username=StringField('Username',validators=[data_required()])
    password=PasswordField('Password',validators=[data_required()])
    remember_me=BooleanField('Remember me')
    submit=SubmitField('Sign in')

class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[data_required(), 
                    Length(min=2,max=20,message='Username length should be between 2 to 20 characters.')])
    email=EmailField('Email', validators=[data_required(), Email("Please enter your email address")])
    password= PasswordField('Password',validators=[data_required()])
    confirm_password= PasswordField('Confirm Password',validators=[data_required(),EqualTo('password')])
    submit=SubmitField('Sign Up')