from flask import Blueprint, request, jsonify
from app.services.encryption_service import encrypt, decrypt

encryption_blueprint = Blueprint('encryption', __name__)


@encryption_blueprint.route('/encrypt', methods=['POST'])
def encrypt_route():
    data = request.get_json()
    result = encrypt(data)
    return result


@encryption_blueprint.route('/decrypt', methods=['POST'])
def decrypt_route():
    data = request.get_json()
    result = decrypt(data)
    return jsonify({'decrypted_data': result})
