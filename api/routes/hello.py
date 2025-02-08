from flask import Blueprint
from sqlalchemy import text
from api.models import db

hello_bp = Blueprint('hello', __name__)

@hello_bp.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"

@hello_bp.route("/test-db")
def test_db():
    try:
        result = db.session.execute(text('SELECT 1')).scalar()
        return f"<p>Database connection successful: {result}</p>"
    except Exception as e:
        return f"<p>Database connection failed: {str(e)}</p>"