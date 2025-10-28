from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from zoneinfo import ZoneInfo

# Association table for many-to-many relationship between Complaint and Department
complaint_departments = db.Table(
    'complaint_departments',
    db.Column('complaint_id', db.Integer, db.ForeignKey('complaint.id'), primary_key=True),
    db.Column('department_id', db.Integer, db.ForeignKey('department.id'), primary_key=True)
)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo("Asia/Kolkata")))
    
    department = db.relationship("Department", backref="users")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    status = db.Column(db.Enum('pending', 'in_progress', 'resolved', name='complaint_status'), default='pending')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo("Asia/Kolkata")))
    image_filenames = db.Column(db.Text)
    resolution_note = db.Column(db.Text, nullable=True)
    resolved_images = db.Column(db.Text, nullable=True)
    
    user = db.relationship('User', backref='complaints', lazy=True)
    departments = db.relationship("Department", secondary=complaint_departments, backref="complaints")
