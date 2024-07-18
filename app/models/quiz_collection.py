from .. import db

class QuizCollection(db.Model):
    __tablename__ = 'quiz_collection'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    thumbnail_url = db.Column(db.Text, nullable=False)  # thumbnail_url 필드를 TEXT로 변경
    views = db.Column(db.Integer, nullable=False,server_default='0')  # 조회수 필드 추가

    quizzes = db.relationship('Quiz', back_populates='quiz_collection', cascade='all, delete-orphan')
