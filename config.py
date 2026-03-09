import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Force reload .env file
load_dotenv(override=True)

class Config:
    """Application configuration"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Database Configuration
    # Check if DATABASE_URL is provided (Railway/Heroku style)
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    if DATABASE_URL:
        # Use DATABASE_URL if provided
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
        # Fix mysql:// to mysql+mysqlconnector://
        if SQLALCHEMY_DATABASE_URI.startswith('mysql://'):
            SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('mysql://', 'mysql+mysqlconnector://', 1)
    else:
        # Fallback to individual env vars
        DB_HOST = os.getenv('DB_HOST', 'localhost')
        DB_PORT = int(os.getenv('DB_PORT', '3306'))
        DB_USER = os.getenv('DB_USER', 'root')
        DB_PASSWORD = os.getenv('DB_PASSWORD', '')
        DB_NAME = os.getenv('DB_NAME', 'railway')
        
        # SQLAlchemy Configuration - URL encode password to handle special characters
        SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG
    
    # Connection Pool Settings for better performance
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,              # Tăng số connections
        'pool_recycle': 1800,         # Recycle sau 30 phút
        'pool_pre_ping': True,        # Test connections trước khi dùng
        'max_overflow': 40,           # Cho phép thêm 40 connections
        'pool_timeout': 30,           # Timeout
        'connect_args': {
            'connect_timeout': 10,
            'charset': 'utf8mb4'
        }
    }
    
    # Application Settings
    APP_NAME = os.getenv('APP_NAME', 'OKI VIETNAM HR')
    DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'vi')
    SUPPORTED_LANGUAGES = ['vi', 'en', 'ja']
    
    # Session Configuration
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 1814400  # 3 weeks in seconds (21 days)
    SESSION_COOKIE_SECURE = not DEBUG  # Only send cookies over HTTPS in production
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Auto logout after inactivity
    AUTO_LOGOUT_DURATION = 1814400  # 3 weeks in seconds (21 days)
    
    # Upload Configuration (if needed)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    
    # Timezone
    TIMEZONE = os.getenv('TIMEZONE', 'Asia/Ho_Chi_Minh')
    
    # Flask-Login
    LOGIN_VIEW = 'login'
    LOGIN_MESSAGE = 'Please log in to access this page.'
    
    # WTForms
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 2592000))  # 30 days
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_COOKIE_SECURE = not DEBUG  # Only send cookies over HTTPS in production
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_COOKIE_SAMESITE = 'Lax'
    
    @staticmethod
    def get_database_url():
        """Get database connection URL"""
        return f"mysql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"
    
    @staticmethod
    def get_config_dict():
        """Get all configuration as dictionary"""
        return {
            'SECRET_KEY': Config.SECRET_KEY,
            'DEBUG': Config.DEBUG,
            'DB_HOST': Config.DB_HOST,
            'DB_PORT': Config.DB_PORT,
            'DB_USER': Config.DB_USER,
            'DB_NAME': Config.DB_NAME,
            'APP_NAME': Config.APP_NAME,
            'DEFAULT_LANGUAGE': Config.DEFAULT_LANGUAGE,
            'TIMEZONE': Config.TIMEZONE,
        }
    
    @staticmethod
    def print_config():
        """Print current configuration (hide sensitive data)"""
        config = Config.get_config_dict()
        print("\n=== Current Configuration ===")
        for key, value in config.items():
            if 'PASSWORD' in key or 'SECRET' in key:
                print(f"{key}: {'*' * 8}")
            else:
                print(f"{key}: {value}")
        print("============================\n")


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


# Select configuration based on environment
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    return config_by_name.get(env, DevelopmentConfig)
