from flask import Blueprint, request, jsonify
from api.models.models import db, User

users_bp = Blueprint('users', __name__)

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
        data = request.get_json()
        new_user = User(
            username=data['username'],
            email=data['email'],
            interests=data.get('interests', []),
            availability=data.get('availability', {})
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.__repr__()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        return jsonify(user.__repr__())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        user = User.query.get_or_404(user_id)
        user.username = data['username']
        user.email = data['email']
        user.interests = data.get('interests', user.interests)
        user.availability = data.get('availability', user.availability)
        db.session.commit()
        return jsonify(user.__repr__())
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