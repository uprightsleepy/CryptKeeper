from flask import Flask, jsonify
from app.routes.encryption_routes import encryption_blueprint


def create_app():
    app = Flask(__name__)

    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify(error=str(e)), 404

    @app.errorhandler(TypeError)
    def handle_type_error(error):
        if 'not JSON serializable' in str(error):
            return jsonify({'error': 'Encrypted data not found or invalid request.'}), 404
        return jsonify({'error': 'An unexpected error occurred.'}), 500

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify(error="An internal error occurred, please try again."), 500

    app.register_blueprint(encryption_blueprint)
    return app
