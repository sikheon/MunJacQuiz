from flask import render_template, request, redirect, url_for, flash, session, jsonify
from . import main
from ..models import db, User
from ..forms import SignupForm , LoginForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['email'] = email
            flash('로그인 성공!', 'success')
            return redirect(url_for('main.main'))
        flash('아이디 또는 비밀번호가 올바르지 않습니다.', 'error')
        return redirect(url_for('main.index'))
    
    return render_template('index.html', form=form)
@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        nickname = form.nickname.data

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('이미 존재하는 이메일입니다.', 'error')
            return redirect(url_for('main.signup'))

        new_user = User(email=email, nickname=nickname)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('회원가입 성공!', 'success')
        return redirect(url_for('main.index'))
 
    return render_template('signup.html', form=form)

@main.route('/check_nickname', methods=['POST'])
def check_nickname():
    data = request.get_json()
    nickname = data.get('nickname')
    if nickname:
        existing_nickname = User.query.filter_by(nickname=nickname).first()
        return jsonify({'available': existing_nickname is None})
    return jsonify({'error': 'Invalid request'}), 400



@main.route('/main')
def main():
    return render_template('main.html')
