from flask import Blueprint, request, jsonify
from api.models import db, User

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify([user.__repr__() for user in users])
    except Exception as e:
        return jsonify({"error": str(e)}), 500