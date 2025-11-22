import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_secret_key'
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_NAME = os.environ.get('DB_NAME', 'university_booking')
    # Parse DB_PORT as integer, fallback to 3306 if invalid
    try:
        DB_PORT = int(os.environ.get('DB_PORT', 3306))
    except (ValueError, TypeError):
        DB_PORT = 3306
