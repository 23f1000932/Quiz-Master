from flask_sqlalchemy import SQLAlchemy


# Initialize SQLAlchemy
db = SQLAlchemy()

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False) 
    full_name = db.Column(db.String(150), nullable=False)
    qualification = db.Column(db.String(150))
    dob = db.Column(db.Date)
    is_admin = db.Column(db.Integer, default=1)
    # scores = db.relationship('Score', backref='user', lazy=True)

# class Subject(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text)
#     chapters = db.relationship('Chapter', backref='subject', lazy=True, cascade='all, delete-orphan')

# class Chapter(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text)
#     subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
#     quizzes = db.relationship('Quiz', backref='chapter', lazy=True, cascade='all, delete-orphan')

# class Quiz(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
#     date_of_quiz = db.Column(db.Date)
#     time_duration = db.Column(db.String(5))  # HH:MM format
#     remarks = db.Column(db.Text)
#     questions = db.relationship('Question', backref='quiz', lazy=True, cascade='all, delete-orphan')