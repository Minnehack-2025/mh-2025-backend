from . import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

# association table for the many-to-many relationship between user and event
participants = db.Table('participants',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(90), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(datetime.timezone.utc))
    interests = db.Column(JSON, default=list)
    availability = db.Column(JSON, default=dict)
    events = db.relationship('Event', secondary=participants, backref=db.backref('participants', lazy=True))

    def __repr__(self):
        return f'<User id={self.id} username={self.username} created_at={self.created_at} email={self.email} interests={self.interests} availability={self.availability}>'
    
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(200), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(datetime.timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('events_created', lazy=True))

    def __repr__(self):
        return f'<Event id={self.id} name={self.name} location={self.location} time={self.time} user_id={self.user_id}>'