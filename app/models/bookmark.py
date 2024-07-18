from .. import db
from .user import User  # User 모델 가져오기
from .quiz_collection import QuizCollection
class Bookmark(db.Model):
    __tablename__ = 'bookmark'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_collection_id = db.Column(db.Integer, db.ForeignKey('quiz_collection.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    user = db.relationship('User', back_populates='bookmarks')
    quiz_collection = db.relationship('QuizCollection', back_populates='bookmarks')

# User 모델에 북마크 관계 추가
User.bookmarks = db.relationship('Bookmark', back_populates='user', cascade='all, delete-orphan')

# QuizCollection 모델에 북마크 관계 추가
QuizCollection.bookmarks = db.relationship('Bookmark', back_populates='quiz_collection', cascade='all, delete-orphan')
