import os
import sys

def force_file_databases():
    """Force the application to use file-based databases"""
    print("🔧 FORCING FILE-BASED DATABASES")
    print("=" * 50)
    
    # Set environment variable to force file databases
    os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    
    # Update config.py temporarily
    config_content = '''
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    
    # FORCE FILE-BASED DATABASES
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
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
'''
    
    with open('config.py', 'w') as f:
        f.write(config_content)
    
    print("✅ Updated config.py to use file-based databases")
    print("📊 Database files that will be created:")
    print("   - app.db (main database)")
    print("   - active_cases.db")
    print("   - completed_cases.db")
    print("\n💡 Restart your Flask application now")

if __name__ == "__main__":
    force_file_databases()