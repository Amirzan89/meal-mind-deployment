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
        with app.app_context():
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
    # Determine environment
    env = os.environ.get('FLASK_ENV', 'railway')
    logger.info(f"Starting application in {env} environment")
    
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