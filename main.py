# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_jwt_extended  import JWTManager, create_access_token, jwt_required, get_jwt_identity
# from backend.models import db, User, Course, Enrollment

# app = Flask(__name__)

# # Configurations
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
# app.config['JWT_SECRET_KEY'] = '3tfhryeyrt3454rtrtur' # Change in production

# # Initialize extensions
# db.init_app(app)
# jwt = JWTManager(app)

# # Create tables
# with app.app_context():
#     db.drop_all()  
#     db.create_all()


# # This is the route to register a new user. It expects a JSON payload with username and password.

# from werkzeug.security import generate_password_hash, check_password_hash
# from textwrap import fill

# @app.route('/register', methods=['POST'])
# def register():
#     data = request.json
#     # using .get instead of [] whcih throws an error if the key is not found
#     username = data.get('username')
#     password = data.get('password')
#     email = data.get('email')

#     # list of complusory field that users must fill in and check if those field are filled in.
#     required = ['username', 'password', 'email']
#     for field in required:
#         if field not in data:
#             return jsonify({"msg": f"Missing {field}"}), 400

#     if User.query.filter_by(username=username).first():
#         return jsonify({"msg": "User already exists"}), 400
    
#     if User.query.filter_by(email=email).first():
#             return jsonify({"msg": "Email already exists"}), 400
    
#     hashed_password = generate_password_hash(password)
#     user = User(username=username, password=hashed_password, email=email)
#     db.session.add(user)
#     db.session.commit()

#     return jsonify({"msg": "User registered successfully"}), 201


# # This is the route to log in a user. It expects a JSON payload with username and password.
# @app.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     user = User.query.filter_by(username=data['username']).first()

#     if not user or not check_password_hash(user.password, data['password']):
#         return jsonify({"msg": "Invalid credentials"}), 401

#     token = create_access_token(identity=user.id)
#     return jsonify({"token": token})


# # this is the route to list all the courses
# @app.route('/courses', methods=['GET'])
# def get_courses():
#     courses = Course.query.all()
#     output = [{"id": course.id, "title": course.title, "description": course.description} for course in courses]
#     return jsonify(output)


# # this is the route to enroll in a course
# @app.route('/enroll/<int:course_id>', methods=['POST'])
# @jwt_required()
# def enroll(course_id):
#     user_id = get_jwt_identity()
#     existing = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()

#     if existing:
#         return jsonify({"msg": "Already enrolled"}), 400

#     enrollment = Enrollment(user_id=user_id, course_id=course_id)
#     db.session.add(enrollment)
#     db.session.commit()

#     return jsonify({"msg": "Enrolled successfully"})



# @app.route('/progress/<int:course_id>', methods=['PATCH'])
# @jwt_required()
# def update_progress(course_id):
#     user_id = get_jwt_identity()
#     data = request.json
#     progress = data.get('progress')

#     enrollment = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()

#     if not enrollment:
#         return jsonify({"msg": "Not enrolled in course"}), 404

#     enrollment.progress = progress
#     db.session.commit()

#     return jsonify({"msg": "Progress updated"})


# from flask import send_file
# import os

# VIDEO_FOLDER = os.path.join(os.getcwd(), 'videos')

# @app.route('/course/<int:course_id>/video', methods=['GET'])
# @jwt_required()
# def stream_video(course_id):
#     user_id = get_jwt_identity()
#     enrollment = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()

#     if not enrollment:
#         return jsonify({"msg": "Not enrolled in course"}), 403

#     course = Course.query.get(course_id)
#     video_path = os.path.join(VIDEO_FOLDER, course.video_url)

#     if not os.path.exists(video_path):
#         return jsonify({"msg": "Video not found"}), 404

#     return send_file(video_path, mimetype='video/mp4')

# @app.route('/seed', methods=['POST'])
# def seed():
#     course1 = Course(title="Python for Beginners", description="Learn Python from scratch", video_url="python.mp4")
#     course2 = Course(title="React Masterclass", description="Master React.js", video_url="react.mp4")
#     db.session.add_all([course1, course2])
#     db.session.commit()
#     return jsonify({"msg": "Courses added"})


# if __name__ == '__main__':
#     app.run(debug=True) 


from backend import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 