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

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False) 
    discription = db.Column(db.String(100),  nullable = True)
    chapter_name = db.relationship('Chapter', backref='Subject', lazy=True)

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    discription = db.Column(db.String(100),  nullable = True)
    no_of_Qusetion = db.Column(db.Integer, default = 1)
    subject_id = db.Column(db.Integer, db.forigenKey('Subject.id'), nullable = False)
    quizzes = db.relationship('Quiz', backref='Chapter', lazy=True)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('Chapter.id'), nullable = False)
    date_of_quiz = db.Column(db.Date)
    time_duration = db.Column(db.string(10)) #HH:MM
    remark = db.Column(db.String(100), nullable = True)
    question = db.relationship('Question', backref = 'Quiz', lazy = True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    quiz_id = db.Column (db.Integer , db.ForigenKey("Quiz.id"), nullable = False)
    q_statement = db.Column(db.String(100), nullable = False)
    o_1 = db.Column(db.String(50), nullable = False)
    o_2 = db.Column(db.String(50), nullable = False)
    o_3 = db.Column(db.String(50), nullable = False)
    o_4 = db.Column(db.String(50), nullable = False)
    correct_option = db.Column(db.Integer, nullable = False)

    