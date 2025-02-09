from flask import Blueprint
from .testdb import testdb_bp
from .events import events_bp
from .users import users_bp

def init_routes(app):
    app.register_blueprint(testdb_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(users_bp)