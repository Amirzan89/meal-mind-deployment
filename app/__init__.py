# backend/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from datetime import timedelta
from config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_env=None):
    app = Flask(__name__)
    
    # Get configuration from environment or argument
    if config_env is None:
        config_env = os.environ.get('FLASK_ENV', 'development')
    
    # Import configuration
    from config import config_dict
    app.config.from_object(config_dict[config_env])
    
    # Print which configuration is being used
    print(f"Running with {config_env} configuration")
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Configure CORS
    CORS(app, 
         resources={r"/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    
    # Add a debug endpoint to test CORS
    @app.route('/api/cors-test', methods=['GET', 'OPTIONS'])
    def cors_test():
        return {'message': 'CORS is working!'}
    
    # Serve frontend static files if they exist
    @app.route('/')
    def index():
        static_dir = os.path.join(app.root_path, 'static')
        if os.path.exists(os.path.join(static_dir, 'index.html')):
            from flask import send_from_directory
            return send_from_directory(static_dir, 'index.html')
        else:
            return "Meal Mind Backend is running!"
    
    # Serve static files (JS, CSS, images)
    @app.route('/<path:filename>')
    def static_files(filename):
        static_dir = os.path.join(app.root_path, 'static')
        if os.path.exists(os.path.join(static_dir, filename)):
            from flask import send_from_directory
            return send_from_directory(static_dir, filename)
        else:
            # If not a static file and frontend exists, serve index.html (SPA routing)
            if os.path.exists(os.path.join(static_dir, 'index.html')):
                from flask import send_from_directory
                return send_from_directory(static_dir, 'index.html')
            else:
                return {"error": "Resource not found"}, 404
    
    @app.route('/api/test', methods=['GET'])
    def test_route():
        return {'message': 'API is working!'}
    
    # Import models (penting untuk migration)
    try:
        print("Importing models...")
        from app.models.user import User, UserProfile
        from app.models.food import Food, Activity
        from app.models.recommendation import DailyRecommendation, DailyCheckin
        print("✓ Models imported successfully")
    except Exception as e:
        print(f"❌ Error importing models: {e}")
        return app
    
    # Register blueprints with error handling
    try:
        print("Importing auth routes...")
        from app.routes.auth import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        print("✓ Auth routes registered")
    except Exception as e:
        print(f"❌ Error with auth routes: {e}")
    
    try:
        print("Importing profile routes...")
        from app.routes.profile import profile_bp
        app.register_blueprint(profile_bp, url_prefix='/api/profile')
        print("✓ Profile routes registered")
    except Exception as e:
        print(f"❌ Error with profile routes: {e}")
    
    try:
        print("Importing recommendation routes...")
        from app.routes.recommendations import recommendations_bp
        app.register_blueprint(recommendations_bp, url_prefix='/api/recommendations')
        print("✓ Recommendation routes registered")
    except Exception as e:
        print(f"❌ Error with recommendation routes: {e}")
    
    try:
        print("Importing activities routes...")
        from app.routes.activities import activities_bp
        app.register_blueprint(activities_bp, url_prefix='/api/activities')
        print("✓ Activities routes registered")
    except Exception as e:
        print(f"❌ Error with activities routes: {e}")
    
    try:
        print("Importing user routes...")
        from app.routes.user import user_bp
        app.register_blueprint(user_bp, url_prefix='/api/user')
        print("✓ User routes registered")
    except Exception as e:
        print(f"❌ Error with user routes: {e}")
    
    try:
        print("Importing progress routes...")
        from app.routes.progress import progress_bp
        app.register_blueprint(progress_bp, url_prefix='/api/progress')
        print("✓ Progress routes registered")
    except Exception as e:
        print(f"❌ Error with progress routes: {e}")
    
    # Setup error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Resource not found"}, 404
        
    @app.errorhandler(500)
    def internal_server_error(error):
        return {"error": "Internal server error"}, 500
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app