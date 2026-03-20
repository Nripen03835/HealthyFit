import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # Use /tmp for SQLite on Vercel (ephemeral but writeable)
    if os.environ.get('VERCEL'):
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join('/tmp', 'healthcare.db')
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'healthcare.db')
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    FITBUDDY_GROQ_KEY = os.environ.get('FITBUDDY_GROQ_KEY')
    FITBUDDY_OPENAI_KEY = os.environ.get('FITBUDDY_OPENAI_KEY')
    RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY')
