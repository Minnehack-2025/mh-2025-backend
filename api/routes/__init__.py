from flask import Blueprint
from .hello import hello_bp

def init_routes(app):
    app.register_blueprint(hello_bp)