import os
import secrets
from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = os.environ.get('SESSION_SECRET', secrets.token_hex(32))

ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

db = SQLAlchemy(app)

if not os.path.exists('uploads'):
    os.makedirs('uploads')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

class PortfolioItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_filename = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'link': self.link,
            'category': self.category,
            'image_url': f'/uploads/{self.image_filename}',
            'created_at': self.created_at.isoformat()
        }

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/index.html')
def index_html():
    return send_from_directory('.', 'index.html')

@app.route('/contact.html')
def contact():
    return send_from_directory('.', 'contact.html')

@app.route('/project.html')
def project():
    return send_from_directory('.', 'project.html')

@app.route('/admin')
def admin():
    return send_from_directory('.', 'admin.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    safe_filename = secure_filename(filename)
    return send_from_directory('uploads', safe_filename)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if data and data.get('password') == ADMIN_PASSWORD:
        session['admin_logged_in'] = True
        return jsonify({'success': True})
    return jsonify({'error': 'Invalid password'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('admin_logged_in', None)
    return jsonify({'success': True})

@app.route('/api/auth-status')
def auth_status():
    return jsonify({'authenticated': session.get('admin_logged_in', False)})

@app.route('/api/items', methods=['GET'])
def get_items():
    items = PortfolioItem.query.order_by(PortfolioItem.created_at.desc()).all()
    return jsonify([item.to_dict() for item in items])

@app.route('/api/items', methods=['POST'])
@admin_required
def create_item():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg, gif, webp'}), 400
    
    original_filename = secure_filename(file.filename)
    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{original_filename}"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    item = PortfolioItem(
        title=request.form['title'],
        description=request.form['description'],
        link=request.form['link'],
        category=request.form['category'],
        image_filename=filename
    )
    db.session.add(item)
    db.session.commit()
    
    return jsonify(item.to_dict()), 201

@app.route('/api/items/<int:id>', methods=['DELETE'])
@admin_required
def delete_item(id):
    item = PortfolioItem.query.get_or_404(id)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], item.image_filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
