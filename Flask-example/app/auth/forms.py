from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, EmailField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)], id="floatingName")
    password = PasswordField('Password', validators=[DataRequired()], id="floatingPassword")
    email = EmailField('Email', validators=[DataRequired(), Email()], id="floatingEmail")
    submit = SubmitField('Registrar')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()], id="floatingEmail")
    password = PasswordField('Password', validators=[DataRequired()], id="floatingPassword")
    remember_me = BooleanField('Recuérdame', id="flexCheckDefault")
    submit = SubmitField('Login')