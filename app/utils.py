from app.models import User, db

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def create_user(email, name, profile_pic=None):
    user = User(email=email, name=name, profile_pic=profile_pic)
    db.session.add(user)
    db.session.commit()
    return user

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
