from flask import Blueprint, request, jsonify
from app.services.encryption_service import encrypt, decrypt
from marshmallow import Schema, fields, ValidationError

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


@encryption_blueprint.route('/decrypt', methods=['POST'])
def decrypt_route():
    schema = EncryptionRequestSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as e:
        return jsonify(e.messages), 400

    result = decrypt(data)
    return jsonify({'decrypted_data': result})
