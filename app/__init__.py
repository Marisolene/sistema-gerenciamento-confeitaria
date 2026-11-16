from flask import Flask
from config import Config
from app.extensions import db


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    with app.app_context():
        from app import models
        db.create_all()

    from app.routes import main
    app.register_blueprint(main)

    return app
