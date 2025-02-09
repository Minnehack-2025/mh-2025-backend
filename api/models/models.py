from . import db
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import JSON
from werkzeug.security import generate_password_hash, check_password_hash

# association table for the many-to-many relationship between user and event
participants = db.Table('participants',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(90), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    interests = db.Column(JSON, default=list)
    availability = db.Column(JSON, default=dict)
    events = db.relationship('Event', secondary=participants, backref=db.backref('participants', lazy=True))
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=True)
    education_level = db.Column(db.String(50), nullable=True)
    preference = db.Column(db.String(50), nullable=True)
    goal = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<User id={self.id} username={self.username} created_at={self.created_at} email={self.email} interests={self.interests} availability={self.availability} image_id={self.image_id} education_level={self.education_level} preference={self.preference} goal={self.goal}>'
    
    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(200), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=True)

    user = db.relationship('User', backref=db.backref('events_created', lazy=True))

    def __repr__(self):
        return f'<Event id={self.id} name={self.name} location={self.location} time={self.time} user_id={self.user_id} image_id={self.image_id}>'

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)

class Statistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(10), nullable=False)
    time_slot = db.Column(db.Integer, nullable=False)
    user_ids = db.Column(JSON, default=list)

    def __repr__(self):
        return f'<Statistics id={self.id} day={self.day} time_slot={self.time_slot} user_ids={self.user_ids}>'