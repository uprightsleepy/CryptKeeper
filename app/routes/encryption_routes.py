import os

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from app.config.constants import ENCRYPT_S3_BUCKET_NAME, DECRYPT_S3_BUCKET_NAME, ENCRYPTED_IDENTIFIER
from app.data.s3_access import upload_file, download_file, upload_bytes
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
        name, extension = os.path.splitext(filename)
        encrypted_filename = f"{name}{ENCRYPTED_IDENTIFIER}{extension}"

        file_content = file.read()
        password, salt = get_secrets()
        encrypted_content = encrypt_file(file_content, password, salt)

        write_to_file(encrypted_filename, encrypted_content)

        object_name = f"encrypted/{encrypted_filename}"
        upload_successful = upload_file(encrypted_filename, ENCRYPT_S3_BUCKET_NAME, object_name)

        if upload_successful:
            message = "File encrypted and uploaded successfully"
        else:
            message = "File encrypted but upload failed"

        return jsonify(message=message, encrypted_file=encrypted_filename)
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
        filename = request.get_json().get('filename')
        if not filename or ENCRYPTED_IDENTIFIER not in filename:
            return jsonify(error="Invalid file name or file does not follow the approved naming convention."), 400

        secure_file_name = secure_filename(filename)

        password, salt = get_secrets()

        encrypted_content = download_file(ENCRYPT_S3_BUCKET_NAME, secure_file_name)

        if encrypted_content is None:
            return jsonify(error="Failed to download file."), 500

        decrypted_content = decrypt_data(encrypted_content, password, salt)

        decrypted_filename = secure_file_name.replace(ENCRYPTED_IDENTIFIER, '')
        decrypted_object_name = f"decrypted/{decrypted_filename}"

        if upload_bytes(decrypted_content, DECRYPT_S3_BUCKET_NAME, decrypted_object_name):
            return jsonify(message="File decrypted and uploaded successfully", decrypted_file=decrypted_object_name)
        else:
            return jsonify(error="Failed to upload decrypted file."), 500
    except ValueError as e:
        return jsonify(error=str(e)), 400
    except Exception as e:
        return jsonify(error=str(e)), 500
