from flask import Flask
from app.routes.encryption_routes import encryption_blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(encryption_blueprint)
    return app
