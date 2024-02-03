from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.services.encryption_service import encrypt, decrypt, decrypt_data, encrypt_file
from marshmallow import Schema, fields, ValidationError

from app.utils.file_manager import write_to_file, validate_and_get_file
from app.utils.secrets_manager import get_secrets

encryption_blueprint = Blueprint('encryption', __name__)


class EncryptionRequestSchema(Schema):
    id = fields.Str(required=True)
    itemType = fields.Str(required=True)
    plaintext = fields.Str(required=False)


@encryption_blueprint.route('/encrypt', methods=['POST'])
def encrypt_route():
    schema = EncryptionRequestSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as e:
        return jsonify(e.messages), 400

    result = encrypt(data)
    return result


@encryption_blueprint.route('/encrypt-file', methods=['POST'])
def encrypt_file_route():
    try:
        file = validate_and_get_file(request)
        filename = secure_filename(file.filename)

        if filename.endswith('.txt'):
            name, extension = filename.rsplit('.txt', 1)
            encrypted_filename = f"{name}_encrypted_.txt"
        else:
            encrypted_filename = filename + '_encrypted_'

        file_content = file.read()

        password, salt = get_secrets()
        encrypted_content = encrypt_file(file_content, password, salt)

        write_to_file(encrypted_filename, encrypted_content)

        return jsonify(message="File encrypted successfully", encrypted_file=encrypted_filename)
    except ValueError as e:
        return jsonify(error=str(e)), 400
    except Exception as e:
        return jsonify(error=str(e)), 500


@encryption_blueprint.route('/decrypt', methods=['POST'])
def decrypt_route():
    schema = EncryptionRequestSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as e:
        return jsonify(e.messages), 400

    result = decrypt(data)
    return jsonify({'decrypted_data': result})


@encryption_blueprint.route('/decrypt-file', methods=['POST'])
def decrypt_file_route():
    try:
        file = validate_and_get_file(request)
        filename = secure_filename(file.filename)
        if '_encrypted_' in filename:
            decrypted_filename = filename.replace('_encrypted_', '')
        else:
            return jsonify(error="File does not appear to be encrypted or does not follow the naming convention"), 400

        file_content = file.read()

        password, salt = get_secrets()
        decrypted_content = decrypt_data(file_content, password, salt)

        write_to_file(decrypted_filename, decrypted_content)

        return jsonify(message="File decrypted successfully", decrypted_file=decrypted_filename)
    except ValueError as e:
        return jsonify(error=str(e)), 400
    except Exception as e:
        return jsonify(error=str(e)), 500
