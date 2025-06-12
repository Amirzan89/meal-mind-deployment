# backend/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-meal-mind'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour for production (can be adjusted)

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    # Use SQLite for development
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///instance/mealmind_dev.db'
    JWT_ACCESS_TOKEN_EXPIRES = False  # No expiration during development

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    # Use in-memory SQLite for tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_ACCESS_TOKEN_EXPIRES = False

class ProductionConfig(Config):
    """Production configuration."""
    # Use Railway DATABASE_URL if available, otherwise use temp SQLite (Railway-friendly)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:////tmp/mealmind.db'
    
    # Production database optimizations (only for PostgreSQL)
    if os.environ.get('DATABASE_URL') and 'postgresql' in os.environ.get('DATABASE_URL', ''):
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_size': 10,
            'max_overflow': 20,
            'pool_recycle': 3600,  # recycle connections after 1 hour
            'pool_pre_ping': True  # verify connections before use
        }
    
    # Security settings
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True

class RailwayConfig(Config):
    """Railway deployment configuration."""
    # Railway provides DATABASE_URL for PostgreSQL addon, otherwise use SQLite fallback
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:////tmp/mealmind.db'
    
    # Use PostgreSQL optimizations only if DATABASE_URL is PostgreSQL
    if os.environ.get('DATABASE_URL') and 'postgresql' in os.environ.get('DATABASE_URL', ''):
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_size': 5,
            'max_overflow': 10,
            'pool_recycle': 3600,
            'pool_pre_ping': True
        }
    
    # Railway-specific settings
    DEBUG = False
    TESTING = False

# Configuration dictionary to easily select environment
config_dict = {
    'development': DevelopmentConfig,
    'testing': TestingConfig, 
    'production': ProductionConfig,
    'railway': RailwayConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Return the appropriate configuration object based on environment."""
    env = os.environ.get('FLASK_ENV', 'development')
    return config_dict.get(env, config_dict['default'])