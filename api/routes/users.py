from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from io import BytesIO
from api.models.models import db, User, Image, Statistics
from werkzeug.security import generate_password_hash, check_password_hash
import json

users_bp = Blueprint('users', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def update_statistics(user_id, availability):
    for day, slots in availability.items():
        for i, available in enumerate(slots):
            if available:
                stat = Statistics.query.filter_by(day=day, time_slot=i).first()
                if stat:
                    if user_id not in stat.user_ids:
                        stat.user_ids.append(user_id)
                else:
                    stat = Statistics(day=day, time_slot=i, user_ids=[user_id])
                db.session.add(stat)
    db.session.commit()

@users_bp.route('/statistics', methods=['GET'])
def get_statistics():
    try:
        statistics = Statistics.query.all()
        stats_dict = {}
        for stat in statistics:
            if stat.day not in stats_dict:
                stats_dict[stat.day] = [[] for _ in range(48)]
            stats_dict[stat.day][stat.time_slot] = stat.user_ids
        return jsonify(stats_dict), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify([user.__repr__() for user in users])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.form.to_dict()
        file = request.files.get('image')
        image_id = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            new_image = Image(filename=filename, data=file.read())
            db.session.add(new_image)
            db.session.commit()
            image_id = new_image.id

        availability = json.loads(data.get('availability', '{}'))

        new_user = User(
            username=data['username'],
            email=data['email'],
            interests=json.loads(data.get('interests', '[]')),
            availability=availability,
            image_id=image_id,
            education_level=data.get('education_level'),
            preference=data.get('preference'),
            goal=data.get('goal')
        )
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()

        update_statistics(new_user.id, new_user.availability)
        
        return jsonify(new_user.__repr__()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.form.to_dict()
        user = User.query.get_or_404(user_id)
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.set_password(data['password'])
        if 'interests' in data:
            user.interests = json.loads(data['interests'])
        if 'availability' in data:
            user.availability = json.loads(data['availability'])
        if 'education_level' in data:
            user.education_level = data['education_level']
        if 'preference' in data:
            user.preference = data['preference']
        if 'goal' in data:
            user.goal = data['goal']
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                new_image = Image(filename=filename, data=file.read())
                db.session.add(new_image)
                db.session.commit()
                user.image_id = new_image.id
        db.session.commit()

        update_statistics(user.id, user.availability)

        return jsonify(user.__repr__()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/users/login', methods=['POST'])
def login_user():
    try:
        data = request.form
        user = User.query.filter_by(email=data['email']).first()
        if user and user.check_password(data['password']):
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500