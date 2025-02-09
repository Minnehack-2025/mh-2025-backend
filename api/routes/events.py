from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from io import BytesIO
from api.models.models import db, Event, Image
from datetime import datetime

events_bp = Blueprint('events', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@events_bp.route('/events', methods=['GET'])
def get_events():
    try:
        number = request.args.get('number', default=10, type=int)
        events = Event.query.limit(number).all()
        return jsonify([event.__repr__() for event in events])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@events_bp.route('/events', methods=['POST'])
def create_event():
    try:
        # Log the incoming request data
        print("Request form data:", request.form)
        print("Request files:", request.files)

        # Parse the request data
        data = request.form.to_dict()
        file = request.files.get('image')
        image_id = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            new_image = Image(filename=filename, data=file.read())
            db.session.add(new_image)
            db.session.commit()
            image_id = new_image.id

        # Create the new event
        new_event = Event(
            name=data['name'],
            description=data.get('description'),
            location=data['location'],
            time=datetime.now(),
            user_id=int(data['user_id']),
            image_id=image_id
        )
        db.session.add(new_event)
        db.session.commit()
        return jsonify(new_event.__repr__()), 201
    except Exception as e:
        print("Error:", str(e))
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
        data = request.form
        event = Event.query.get_or_404(event_id)
        if 'name' in data:
            event.name = data['name']
        if 'description' in data:
            event.description = data.get('description')
        if 'location' in data:
            event.location = data['location']
        if 'time' in data:
            event.time = datetime.strptime(data['time'], '%Y-%m-%dT%H:%M:%S')

        file = request.files.get('image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            new_image = Image(filename=filename, data=file.read())
            db.session.add(new_image)
            db.session.commit()
            event.image_id = new_image.id

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