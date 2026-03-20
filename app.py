from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import requests
from config import Config
from models import db, User, Report, Medicine, Exercise, FitnessPlan, GymPlan
from forms import RegistrationForm, LoginForm, ProfileForm, ReportForm, FitnessForm, GymForm
from utils.ocr_helper import extract_text_from_image, extract_text_from_pdf
from utils.medicine_db import search_medicine
from utils.report_analyzer import analyze_report_with_openai
from utils.fitness_planner import generate_bodyweight_plan
from utils.gym_planner import generate_gym_plan, calculate_water_intake
import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Configure uploads for Vercel environment (using /tmp)
if os.environ.get('VERCEL'):
    app.config['UPLOAD_FOLDER'] = os.path.join('/tmp', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Ensure DB is initialized for serverless environments
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(
            email=form.email.data,
            password_hash=hashed_pw,
            name=form.name.data,
            age=form.age.data,
            current_weight=form.current_weight.data,
            target_weight=form.target_weight.data,
            body_structure=form.body_structure.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    reports = Report.query.filter_by(user_id=current_user.id).order_by(Report.created_at.desc()).limit(5).all()
    fitness_plan = FitnessPlan.query.filter_by(user_id=current_user.id).order_by(FitnessPlan.created_at.desc()).first()
    gym_plan = GymPlan.query.filter_by(user_id=current_user.id).order_by(GymPlan.created_at.desc()).first()
    return render_template('dashboard.html', reports=reports, fitness_plan=fitness_plan, gym_plan=gym_plan)

@app.route('/chatbot')
@login_required
def chatbot():
    return render_template('chatbot.html')

@app.route('/chatbot/api', methods=['POST'])
@login_required
def chatbot_api():
    data = request.get_json()
    query = data.get('query', '').strip()
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    import json
    from groq import Groq as GroqClient
    groq_key = app.config['GROQ_API_KEY']
    prompt = f"Provide comprehensive medicine information for '{query}'. Return ONLY a valid JSON object with EXACTLY these keys: 'name', 'uses', 'dosage', 'side_effects', 'precautions'. Do not include any markdown, code fences, or extra text."
    try:
        client = GroqClient(api_key=groq_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert pharmacist AI. Only output valid JSON with no extra text."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400
        )
        ans = response.choices[0].message.content.strip()
        if ans.startswith('```json'):
            ans = ans[7:]
        if ans.startswith('```'):
            ans = ans[3:]
        if ans.endswith('```'):
            ans = ans[:-3]
        return jsonify(json.loads(ans.strip()))
    except Exception as e:
        # Fallback to local DB
        medicine = search_medicine(query)
        if medicine:
            return jsonify({'name': medicine.name, 'uses': medicine.uses, 'dosage': medicine.dosage, 'side_effects': medicine.side_effects, 'precautions': medicine.precautions})
        return jsonify({'error': f'Medicine not found or API error: {str(e)}'}), 404

@app.route('/chatbot/upload-image', methods=['POST'])
@login_required
def chatbot_upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        text = extract_text_from_image(filepath)
        if not text:
            return jsonify({'error': 'Could not extract text from image. Ensure the image is clear.'}), 400
            
        words = [w.strip() for w in text.split('\n') if w.strip()]
        for word in words:
            first_term = word.split()[0] if word else ""
            if len(first_term) > 3:
                medicine = search_medicine(first_term)
                if medicine:
                    return jsonify({
                        'name': medicine.name,
                        'uses': medicine.uses,
                        'dosage': medicine.dosage,
                        'side_effects': medicine.side_effects,
                        'precautions': medicine.precautions,
                        'detected_text': word
                    })
                
        return jsonify({'error': f'Medicine not found based on detected text: "{text[:50]}..."'}), 404

@app.route('/fitbuddy')
@login_required
def fitbuddy():
    return render_template('fitbuddy.html')

@app.route('/fitbuddy/api', methods=['POST'])
@login_required
def fitbuddy_api():
    data = request.get_json()
    query = data.get('query', '').strip()
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    from groq import Groq as GroqClient
    groq_key = app.config['GROQ_API_KEY']
    if not groq_key:
        return jsonify({'error': 'Groq API key not configured.'}), 500
    try:
        client = GroqClient(api_key=groq_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are FitBuddy, an all-rounder fitness and health AI assistant. Keep responses helpful, friendly, and concise."},
                {"role": "user", "content": query}
            ],
            max_tokens=600
        )
        return jsonify({'response': response.choices[0].message.content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/report-analyzer', methods=['GET', 'POST'])
@login_required
def report_analyzer():
    form = ReportForm()
    if form.validate_on_submit():
        file = form.report.data
        text_content = form.text_content.data
        extracted_text = ""
        
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            ext = filename.lower().split('.')[-1]
            if ext in ['png', 'jpg', 'jpeg', 'gif', 'bmp']:
                extracted_text = extract_text_from_image(filepath)
            elif ext == 'pdf':
                extracted_text = extract_text_from_pdf(filepath)
            elif ext == 'docx':
                try:
                    from docx import Document
                    doc = Document(filepath)
                    extracted_text = '\n'.join([para.text for para in doc.paragraphs])
                except Exception as e:
                    extracted_text = f"Error reading DOCX: {e}"
            else:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        extracted_text = f.read()
                except UnicodeDecodeError:
                    extracted_text = "Error: File encoding not supported."
        elif text_content:
            extracted_text = text_content
        else:
            flash('Please provide a file or text.', 'warning')
            return redirect(url_for('report_analyzer'))
        
        analysis = analyze_report_with_openai(extracted_text)
        
        report = Report(
            user_id=current_user.id,
            filename=file.filename if file else 'text_input',
            extracted_text=extracted_text[:500] + '...' if len(extracted_text) > 500 else extracted_text,
            summary=analysis['summary'],
            recommendation=analysis['recommendation']
        )
        db.session.add(report)
        db.session.commit()
        return render_template('report_result.html', report=report, explanation=analysis.get('explanation', ''))
        
    return render_template('report_analyzer.html', form=form)

@app.route('/fitness-trainer', methods=['GET', 'POST'])
@login_required
def fitness_trainer():
    form = FitnessForm()
    if request.method == 'GET':
        form.current_weight.data = current_user.current_weight
        form.target_weight.data = current_user.target_weight
        form.body_structure.data = current_user.body_structure
        
    if form.validate_on_submit():
        plan = generate_bodyweight_plan(
            current_weight=form.current_weight.data or current_user.current_weight,
            target_weight=form.target_weight.data or current_user.target_weight,
            body_structure=form.body_structure.data or current_user.body_structure,
            fitness_level=form.fitness_level.data,
            health_issues=form.health_issues.data
        )
        fitness_plan = FitnessPlan(
            user_id=current_user.id,
            plan_details=plan
        )
        db.session.add(fitness_plan)
        db.session.commit()
        return render_template('fitness_plan.html', plan=plan)
        
    return render_template('fitness_trainer.html', form=form)

@app.route('/gym-trainer', methods=['GET', 'POST'])
@login_required
def gym_trainer():
    form = GymForm()
    muscle_groups = db.session.query(Exercise.muscle_group).distinct().all()
    form.target_muscles.choices = [(mg[0], mg[0]) for mg in muscle_groups if mg[0]]
    
    if request.method == 'GET':
        form.current_weight.data = current_user.current_weight
        form.target_weight.data = current_user.target_weight
        form.body_structure.data = current_user.body_structure
        
    if form.validate_on_submit():
        plan = generate_gym_plan(
            current_weight=form.current_weight.data or current_user.current_weight,
            target_weight=form.target_weight.data or current_user.target_weight,
            body_structure=form.body_structure.data or current_user.body_structure,
            target_muscles=form.target_muscles.data,
            days_per_week=form.days_per_week.data,
            exercises_per_day=form.exercises_per_day.data
        )
        gym_plan = GymPlan(
            user_id=current_user.id,
            plan_details=plan
        )
        db.session.add(gym_plan)
        db.session.commit()
        water = calculate_water_intake(form.current_weight.data or current_user.current_weight, activity_level='high')
        return render_template('gym_plan.html', plan=plan, water_intake=water)
        
    return render_template('gym_trainer.html', form=form)

@app.route('/gym-trainer/exercise/<int:exercise_id>/3d')
@login_required
def get_exercise_3d(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    return jsonify({'model_path': exercise.threeD_model_path, 'name': exercise.name})

@app.route('/api/exercise/video/<path:exercise_name>')
@login_required
def get_exercise_video(exercise_name):
    url = "https://google-search74.p.rapidapi.com/"
    querystring = {"query": f"site:youtube.com {exercise_name} form tutorial", "limit": "1"}
    headers = {
        "x-rapidapi-key": app.config['RAPIDAPI_KEY'],
        "x-rapidapi-host": "google-search74.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        if data.get("results") and len(data["results"]) > 0:
            video_url = data["results"][0]["url"].replace('\\/', '/')
            video_id = None
            if 'watch?v=' in video_url:
                video_id = video_url.split('watch?v=')[1].split('&')[0][:11]
            elif 'shorts/' in video_url:
                video_id = video_url.split('shorts/')[1].split('?')[0][:11]
            elif 'youtu.be/' in video_url:
                video_id = video_url.split('youtu.be/')[1].split('?')[0][:11]
            
            if video_id:
                return jsonify({"video_id": video_id})
    except Exception as e:
        print("RapidAPI Error:", e)
    return jsonify({"error": "Video not found"}), 404

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.age = form.age.data
        current_user.current_weight = form.current_weight.data
        current_user.target_weight = form.target_weight.data
        current_user.body_structure = form.body_structure.data
        db.session.commit()
        flash('Profile updated.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('profile.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)

