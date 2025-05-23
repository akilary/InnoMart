from flask import Flask

from config import Config
from .admin import init_admin
from .extensions import db, login_manager
from .routes import main_bp, auth_bp, profile_bp


def create_app() -> Flask:
    """Создание приложения Flask"""
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    init_admin(app)

    for bp in [main_bp, auth_bp, profile_bp]:
        app.register_blueprint(bp)

    return app
