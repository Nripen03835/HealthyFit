from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    current_weight = db.Column(db.Float)   # in kg
    target_weight = db.Column(db.Float)
    body_structure = db.Column(db.String(50))  # slim, muscular, athletic
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    reports = db.relationship('Report', backref='user', lazy=True)
    fitness_plans = db.relationship('FitnessPlan', backref='user', lazy=True)
    gym_plans = db.relationship('GymPlan', backref='user', lazy=True)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(200))
    extracted_text = db.Column(db.Text)
    summary = db.Column(db.Text)
    recommendation = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    uses = db.Column(db.Text)
    dosage = db.Column(db.String(200))
    side_effects = db.Column(db.Text)
    precautions = db.Column(db.Text)

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    muscle_group = db.Column(db.String(50))
    equipment = db.Column(db.String(100))  # "none" for bodyweight, "dumbbell", "barbell", etc.
    description = db.Column(db.Text)
    sets_reps = db.Column(db.String(50))
    posture_tips = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    threeD_model_path = db.Column(db.String(200))

class FitnessPlan(db.Model):  # Bodyweight plan
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_details = db.Column(db.JSON)  # store workout schedule, exercises, nutrition
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class GymPlan(db.Model):  # Gym plan
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_details = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
