from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from io import BytesIO
from ..models.models import db, Image

images_bp = Blueprint('images', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@images_bp.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        new_image = Image(filename=filename, data=file.read())
        db.session.add(new_image)
        db.session.commit()
        return jsonify({"message": "File uploaded successfully", "id": new_image.id}), 201
    return jsonify({"error": "File type not allowed"}), 400

@images_bp.route('/uploads/<int:image_id>', methods=['GET'])
def serve_image(image_id):
    image = Image.query.get_or_404(image_id)
    return send_file(BytesIO(image.data), mimetype='image/jpeg', as_attachment=False, download_name=image.filename)