import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app)

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register Blueprints
    from app.routes.auth import auth_bp, init_oauth
    app.register_blueprint(auth_bp)
    init_oauth(app)  # Initialize Google OAuth
    
    from app.routes.patient import patient_bp
    app.register_blueprint(patient_bp)
    
    from app.routes.doctor import doctor_bp
    app.register_blueprint(doctor_bp)
    
    from app.routes.hospital import hospital_bp
    app.register_blueprint(hospital_bp)
    
    from app.routes.medical import medical_bp
    app.register_blueprint(medical_bp)
    
    from app.routes.payment import payment_bp
    app.register_blueprint(payment_bp)

    from app.routes.ai import ai_bp
    app.register_blueprint(ai_bp)
    
    from datetime import datetime, timezone
    @app.context_processor
    def inject_now():
        return {'now': lambda: datetime.now(timezone.utc)}

    return app
