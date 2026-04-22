from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect

from app.config import get_config
from app.models import db


def create_app() -> Flask:
    """
    Создает экземпляр приложения.
    """
    app = Flask(__name__)
    app.config.from_object(get_config())

    db.init_app(app)
    CSRFProtect(app)

    from app.routes import user_bp
    app.register_blueprint(user_bp)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    return app
