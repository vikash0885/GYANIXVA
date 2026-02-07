from flask import Flask
from config import Config
from app.extensions import db, login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.chat import chat
    from app.routes.tools import tools
    from app.routes.resources import resources
    from app.routes.ai_features import ai_features
    from app.routes.community import community
    from app.routes.admin import admin
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(chat)
    app.register_blueprint(tools)
    app.register_blueprint(resources)
    app.register_blueprint(ai_features)
    app.register_blueprint(community)
    app.register_blueprint(admin)

    # Create database structure if not exists
    with app.app_context():
        db.create_all()

    # Auto-login Guest Middleware (Removes Login Requirement)
    from app.models import User
    from flask_login import login_user, current_user
    from flask import request
    
    @app.before_request
    def auto_login_guest():
        if not current_user.is_authenticated:
            # Skip static files
            if request.endpoint and 'static' in request.endpoint:
                return

            try:
                guest = User.query.filter_by(username='guest').first()
                if not guest:
                    guest = User(
                        full_name='Guest Student',
                        username='guest',
                        email='guest@example.com'
                    )
                    guest.set_password('guest')
                    db.session.add(guest)
                    db.session.commit()
                
                login_user(guest)
            except Exception as e:
                # Handle DB not ready case (e.g. during first run)
                pass

    return app
