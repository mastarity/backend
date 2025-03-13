from flask_sqlalchemy  import SQLAlchemy

# create an instance of SQLAlchemy

db = SQLAlchemy()

# class User(db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)
#     role = db.Column(db.String(20), nullable=False)
#     enrolled_courses = db.relationship('Enrollment', backref='user', lazy=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    enrolled_courses = db.relationship('Enrollment', backref='user', lazy=True)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(200), nullable=False) 
    description = db.Column(db.Text, nullable=True) 
    video_url = db.Column(db.String(500), nullable=False)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False) 
    progress = db.Column(db.Float, default=0.0)
