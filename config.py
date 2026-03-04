"""Flask application factory."""
from __future__ import annotations

from flask import Flask
from flask_login import current_user

from app.config import Config
from app.controllers.auth_controller import auth_bp
from app.controllers.dashboard_controller import dashboard_bp
from app.controllers.task_controller import task_bp
from app.extensions import csrf, db, login_manager, migrate
from app.models import User


@login_manager.user_loader
def load_user(user_id: str):
    """Reload user from session."""
    return User.query.get(int(user_id))


def create_app(config_object: type[Config] = Config) -> Flask:
    """Create and configure Flask app instance."""
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(dashboard_bp)

    @app.context_processor
    def inject_current_user():
        return {"current_user": current_user}

    return app
