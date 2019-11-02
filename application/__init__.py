from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import api

# Globally accessible libraries
db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)

    with app.app_context():
        from . import routes

        app.register_blueprint(api.api_bp)

        return app
