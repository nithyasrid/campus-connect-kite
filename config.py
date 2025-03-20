import os

class Config:
    # Flask Secret Key (for session management and security)
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')

    # MySQL Database Configuration
    MYSQL_HOST = os.getenv('MYSQL_HOST', '3306')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'YES')  # Change to your actual MySQL password
    MYSQL_DB = os.getenv('MYSQL_DB', 'campus_connect')
    MYSQL_CURSORCLASS = 'DictCursor'
