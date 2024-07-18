from .. import db

class Quiz(db.Model):
    __tablename__ = 'quiz'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String(255), nullable=False)
    question_image_url = db.Column(db.String(200), nullable=True)  # 퀴즈 문제 사진 URL
    answer = db.Column(db.String(255), nullable=False)
    answer_image_url = db.Column(db.String(200), nullable=True)  # 퀴즈 정답 사진 URL
    quiz_collection_id = db.Column(db.Integer, db.ForeignKey('quiz_collection.id'), nullable=False)

    quiz_collection = db.relationship('QuizCollection', back_populates='quizzes')
