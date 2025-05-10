import os

class Config:
    # Secret key for sessions and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key_here'
    
    # Database configurations
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = ''
    DB_NAME = 'agrimart'

    # Email configurations for password reset
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465  # SSL
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'agrimart.batstate.u@gmail.com'
    MAIL_PASSWORD = 'wrcg qudb rjaq etuh'
    MAIL_DEFAULT_SENDER = 'agrimart.batstate.u@gmail.com'
