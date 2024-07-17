from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class SignupForm(FlaskForm):
    email = StringField('이메일', validators=[DataRequired(), Email()])
    password = PasswordField('비밀번호', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('비밀번호 재확인', validators=[DataRequired(), EqualTo('password')])
    nickname = StringField('닉네임', validators=[DataRequired(), Length(min=3, max=20)])
    submit = SubmitField('가입하기')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')