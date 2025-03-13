from flask import Blueprint, request, jsonify
from flask_jwt_extended  import jwt_required, get_jwt_identity
from backend.models import db, Course, Enrollment
from flask import send_file
import os


courses = Blueprint('courses', __name__)


# this is the route to list all the courses
@courses.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    output = [{"id": course.id, "title": course.title, "description": course.description} for course in courses]
    return jsonify(output)


# this is the route to enroll in a course (protected route)
@courses.route('/enroll/<int:course_id>', methods=['POST'])
@jwt_required()
def enroll(course_id):
    user_id = get_jwt_identity()
    course = Course.query.get(course_id)
    existing = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()

    if existing:
        return jsonify({"msg": "Already enrolled"}), 400
    if not course:
        return jsonify({"msg": "Course not found"}), 404

    enrollment = Enrollment(user_id=user_id, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()

    return jsonify({"msg": "Enrolled successfully"})



@courses.route('/progress/<int:course_id>', methods=['PATCH'])
@jwt_required()
def update_progress(course_id):
    user_id = get_jwt_identity()
    data = request.json
    progress = data.get('progress')

    enrollment = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()

    if not enrollment:
        return jsonify({"msg": "Not enrolled in course"}), 404

    enrollment.progress = progress
    db.session.commit()

    return jsonify({"msg": "Progress updated"})


# This route server the course video to the user

VIDEO_FOLDER = os.path.join(os.getcwd(), 'videos')

@courses.route('/course/<int:course_id>/video', methods=['GET'])
@jwt_required()
def stream_video(course_id):
    user_id = get_jwt_identity()
    enrollment = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()

    if not enrollment:
        return jsonify({"msg": "Not enrolled in course"}), 403

    course = Course.query.get(course_id)
    video_path = os.path.join(VIDEO_FOLDER, course.video_url)

    if not os.path.exists(video_path):
        return jsonify({"msg": "Video not found"}), 404

    return send_file(video_path, mimetype='video/mp4')

@courses.route('/seed', methods=['POST'])
def seed():
    course1 = Course(title="Python for Beginners", description="Learn Python from scratch", video_url="python.mp4")
    course2 = Course(title="React Masterclass", description="Master React.js", video_url="react.mp4")
    db.session.add_all([course1, course2])
    db.session.commit()
    return jsonify({"msg": "Courses added"})
