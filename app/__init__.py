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

    return app
