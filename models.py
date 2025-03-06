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
    is_admin = db.Column(db.Boolean, default=False)
    # scores = db.relationship('Score', backref='user', lazy=True)