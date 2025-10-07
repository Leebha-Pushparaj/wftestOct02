import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    
    # Server configuration from environment variables
    SERVER_NAME = os.environ.get('SERVER_NAME') 
    HOST = os.environ.get('FLASK_HOST') 
    PORT = int(os.environ.get('FLASK_PORT') or 5000)
    
    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///main.db'
    SQLALCHEMY_BINDS = {
        'active_cases': 'sqlite:///active_cases.db',
        'completed_cases': 'sqlite:///completed_cases.db'
    }
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') 
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')