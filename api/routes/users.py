from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from io import BytesIO
from api.models.models import db, User, Image
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint('users', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        data = request.form
        file = request.files.get('image')
        image_id = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            new_image = Image(filename=filename, data=file.read())
            db.session.add(new_image)
            db.session.commit()
            image_id = new_image.id

        new_user = User(
            username=data['username'],
            email=data['email'],
            interests=data.get('interests', []),
            availability=data.get('availability', {}),
            image_id=image_id
        )
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.__repr__()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.form
        user = User.query.get_or_404(user_id)
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'interests' in data:
            user.interests = data.get('interests', user.interests)
        if 'availability' in data:
            user.availability = data.get('availability', user.availability)
        if 'password' in data:
            user.set_password(data['password'])

        file = request.files.get('image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            new_image = Image(filename=filename, data=file.read())
            db.session.add(new_image)
            db.session.commit()
            user.image_id = new_image.id

        db.session.commit()
        return jsonify(user.__repr__())
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