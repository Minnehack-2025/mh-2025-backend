from flask import Blueprint
from sqlalchemy import text
from api.models import db

testdb_bp = Blueprint('testdb', __name__)

@testdb_bp.route("/test-db")
def test_db():
    try:
        result = db.session.execute(text('SELECT 1')).scalar()
        return f"<p>Welcome to Caden's super awesome api!</p><p>Database connection successful: {result}</p>"
    except Exception as e:
        return f"<p>Welcome to Caden's somewhat awesome api!</p><p>Database connection failed: {str(e)}</p>"