from flask import Flask

from config import Config
from .routes.auth_routes import auth_bp
from .routes.debug_routes import debug_bp
from .services.db_service import close_db, init_db


def create_app() -> Flask:
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(Config)
    app.register_blueprint(auth_bp)
    app.register_blueprint(debug_bp)
    app.teardown_appcontext(close_db)

    with app.app_context():
        init_db()

    return app
