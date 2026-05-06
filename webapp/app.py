from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)

# Database Configuration - PostgreSQL
database_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/appdb')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

db = SQLAlchemy(app)

# User Model - Defines the structure of data stored in PostgreSQL
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

# Create tables within application context
with app.app_context():
    db.create_all()

# Route: Homepage - Tests database connection
@app.route('/')
def home():
    try:
        user_count = User.query.count()
        db_status = "Connected"
    except Exception as e:
        db_status = f"Error: {str(e)}"
        user_count = 0
    
    return jsonify({
        'message': 'Welcome to Flask CI/CD App!',
        'status': 'running',
        'database': db_status,
        'user_count': user_count,
        'timestamp': datetime.utcnow().isoformat()
    })

# Route: Health Check - Used by Docker and Jenkins
@app.route('/health')
def health():
    try:
        db.session.execute('SELECT 1')
        db_status = 'healthy'
    except Exception as e:
        db_status = 'unhealthy'
    
    return jsonify({
        'status': 'ok',
        'database': db_status,
        'service': 'webapp'
    })

# Route: Get all users from database
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# Route: Create new user in database
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email'):
        return jsonify({'error': 'username and email required'}), 400
    
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],
        password=data.get('password', 'default123')
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201

# Route: Login endpoint for Selenium testing
@app.route('/login', methods=['GET'])
def login_page():
    return jsonify({
        'message': 'Login page',
        'status': 'ready',
        'requires': ['username', 'password']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
