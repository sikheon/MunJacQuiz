from flask import render_template, request, redirect, url_for, flash, session, jsonify
from . import main
from ..models import db, User, QuizCollection, Quiz, Bookmark
from ..forms import SignupForm , LoginForm
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['email'] = email
            session['nickname'] = user.nickname
            flash('로그인 성공!', 'success')
            return redirect(url_for('main.dashboard'))
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

@main.route('/dashboard')
@login_required
def dashboard():
    recommended_quiz_collections = QuizCollection.query.order_by(QuizCollection.views.desc()).limit(12).all()
    all_quiz_collections = QuizCollection.query.all()
    
    # 현재 사용자의 북마크된 퀴즈 컬렉션 가져오기
    user = User.query.filter_by(email=session['email']).first()
    bookmarked_collections = [bookmark.quiz_collection for bookmark in user.bookmarks]
    
    return render_template('dashboard.html', 
                           recommended_quiz_collections=recommended_quiz_collections,
                           all_quiz_collections=all_quiz_collections,
                           bookmarked_collections=bookmarked_collections)

@main.route('/toggle_bookmark/<int:quiz_collection_id>', methods=['POST'])
@login_required
def toggle_bookmark(quiz_collection_id):
    user = User.query.filter_by(email=session['email']).first()
    bookmark = Bookmark.query.filter_by(user_id=user.id, quiz_collection_id=quiz_collection_id).first()
    
    if bookmark:
        db.session.delete(bookmark)
        db.session.commit()
        return jsonify({'status': 'removed'})
    else:
        new_bookmark = Bookmark(user_id=user.id, quiz_collection_id=quiz_collection_id)
        db.session.add(new_bookmark)
        db.session.commit()
        return jsonify({'status': 'added'})

@main.route('/game_start', methods=['GET'])
@login_required
def game_start():
    quiz_id = request.args.get('quiz_id', type=int)
    quiz_collection = QuizCollection.query.get(quiz_id)
    if quiz_collection:
        quiz_collection.views += 1
        db.session.commit()
    return render_template('game_start.html', quiz_id=quiz_id)




@main.route('/logout')
@login_required
def logout():
    # 세션에서 사용자 정보 제거
    session.pop('email', None)
    session.pop('nickname', None)
    
    # 로그아웃 메시지 표시
    flash('성공적으로 로그아웃되었습니다.', 'success')
    
    # 인덱스 페이지로 리다이렉트
    return redirect(url_for('main.index'))







