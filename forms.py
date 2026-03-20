from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField, SelectField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    name = StringField('Full Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[Optional()])
    current_weight = FloatField('Current Weight (kg)', validators=[Optional()])
    target_weight = FloatField('Target Weight (kg)', validators=[Optional()])
    body_structure = SelectField('Desired Body Structure', choices=[('', 'Select...'), ('slim', 'Slim'), ('muscular', 'Muscular'), ('athletic', 'Athletic')], validators=[Optional()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[Optional()])
    current_weight = FloatField('Current Weight (kg)', validators=[Optional()])
    target_weight = FloatField('Target Weight (kg)', validators=[Optional()])
    body_structure = SelectField('Desired Body Structure', choices=[('slim', 'Slim'), ('muscular', 'Muscular'), ('athletic', 'Athletic')], validators=[Optional()])
    submit = SubmitField('Update')

class ReportForm(FlaskForm):
    report = FileField('Upload Report (Image, PDF, DOCX, TXT)', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'pdf', 'docx', 'txt'], 'Only images, PDFs, DOCX, and TXT files allowed!')])
    text_content = TextAreaField('Or paste text here')
    submit = SubmitField('Analyze')

class FitnessForm(FlaskForm):
    current_weight = FloatField('Current Weight (kg)', validators=[Optional()])
    target_weight = FloatField('Target Weight (kg)', validators=[Optional()])
    body_structure = SelectField('Desired Body Structure', choices=[('slim', 'Slim'), ('muscular', 'Muscular'), ('athletic', 'Athletic')], validators=[Optional()])
    fitness_level = SelectField('Fitness Level', choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], validators=[DataRequired()])
    health_issues = TextAreaField('Any health issues/injuries? (optional)')
    submit = SubmitField('Generate Plan')

class GymForm(FlaskForm):
    current_weight = FloatField('Current Weight (kg)', validators=[Optional()])
    target_weight = FloatField('Target Weight (kg)', validators=[Optional()])
    body_structure = SelectField('Desired Body Structure', choices=[('slim', 'Slim'), ('muscular', 'Muscular'), ('athletic', 'Athletic')], validators=[Optional()])
    target_muscles = SelectMultipleField('Target Muscles', choices=[], validators=[DataRequired()])
    days_per_week = SelectField('Days per week', choices=[('3', '3 days'), ('4', '4 days'), ('5', '5 days'), ('6', '6 days')], validators=[DataRequired()])
    exercises_per_day = SelectField('Exercises per day', choices=[('1', '1 exercise'), ('2', '2 exercises'), ('3', '3 exercises'), ('4', '4 exercises')], validators=[DataRequired()], default='3')
    submit = SubmitField('Generate Plan')
