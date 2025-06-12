#!/usr/bin/env python3
"""
Railway deployment startup script
Handles database initialization and starts the Flask app
"""
import os
import sys
import logging
from app import create_app, db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_database(app):
    """Initialize database tables"""
    try:
        # Ensure database directories exist
        os.makedirs('/tmp', exist_ok=True)
        os.makedirs('/app/instance', exist_ok=True)
        logger.info("Database directories created")
        
        with app.app_context():
            # Log the actual database URL being used
            logger.info(f"Using database: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
            # Create all tables
            db.create_all()
            logger.info("Database tables created successfully")
            
            # Seed basic data if needed
            from app.models.user import User
            if not User.query.first():
                logger.info("Database is empty, seeding basic data...")
                from app.cli import seed_db
                seed_db()
                
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

def main():
    """Main startup function"""
    # Determine environment - Railway often sets FLASK_ENV=production
    env = os.environ.get('FLASK_ENV', 'production')
    logger.info(f"Starting application in {env} environment")
    
    # Log database configuration for debugging
    db_url = os.environ.get('DATABASE_URL', 'Not set')
    railway_env = os.environ.get('RAILWAY_ENVIRONMENT', 'Not set')  
    port_env = os.environ.get('PORT', 'Not set')
    logger.info(f"DATABASE_URL: {db_url}")
    logger.info(f"RAILWAY_ENVIRONMENT: {railway_env}")
    logger.info(f"PORT: {port_env}")
    
    # Create Flask app
    app = create_app(env)
    
    # Initialize database
    initialize_database(app)
    
    # Get port from environment (Railway sets this)
    port = int(os.environ.get('PORT', 5000))
    
    # Start the application
    logger.info(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    main() 