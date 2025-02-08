from flask import Blueprint

hello_bp = Blueprint('hello', __name__)

@hello_bp.route("/api/hello")
def hello_world():
    return "<p>Hello, World!</p>"

@hello_bp.route("/api/goodbye")
def goodbye_world():
    return "<p>Goodbye, World!</p>"

@hello_bp.route("/api/custom/<name>")
def custom_greeting(name):
    return f"<p>Hello, {name}!</p>"