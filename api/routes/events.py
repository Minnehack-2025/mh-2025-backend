from flask import Blueprint, request, jsonify
from api.models import db, User, Event
from datetime import datetime

events_bp = Blueprint('events', __name__)

@events_bp.route('/events', methods=['GET'])
def get_events():
    try:
        number = request.args.get('number', default=10, type=int)
        events = Event.query.limit(number).all()
        return jsonify([event.__repr__()] for event in events)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@events_bp.route('/events', methods=['POST'])
def create_event():
    try:
        data = request.get_json()
        new_event = Event(
            name=data['name'],
            description=data.get('description'),
            location=data['location'],
            time=datetime.strptime(data['time'], '%Y-%m-%dT%H:%M:%S'),
            user_id=data['user_id']
        )
        db.session.add(new_event)
        db.session.commit()
        return jsonify(new_event.__repr__()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@events_bp.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    try:
        event = Event.query.get_or_404(event_id)
        return jsonify(event.__repr__())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@events_bp.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    try:
        data = request.get_json()
        event = Event.query.get_or_404(event_id)
        event.name = data['name']
        event.description = data.get('description')
        event.location = data['location']
        event.time = datetime.strptime(data['time'], '%Y-%m-%dT%H:%M:%S')
        db.session.commit()
        return jsonify(event.__repr__())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@events_bp.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    try:
        event = Event.query.get_or_404(event_id)
        db.session.delete(event)
        db.session.commit()
        return '', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500