from base64 import b64encode

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
from flask import jsonify
from app.config.constants import ENCRYPT_DECRYPT_PASSWORD_SECRET_NAME, ENCRYPT_DECRYPT_SALT_SECRET_NAME, \
    ENCODING_STANDARD
from app.data.dynamodb_access import create_table_item, retrieve_item_by_id
from app.utils.secrets_manager import get_secret


def encrypt(data):
    try:
        plaintext = data.get('plaintext')
        password = get_secret(ENCRYPT_DECRYPT_PASSWORD_SECRET_NAME)
        salt = get_secret(ENCRYPT_DECRYPT_SALT_SECRET_NAME)

        key = PBKDF2(password, salt, dkLen=32)
        cipher = AES.new(key, AES.MODE_CBC)
        padded_plaintext = pad(plaintext.encode(ENCODING_STANDARD), AES.block_size)
        ciphered_data = cipher.encrypt(padded_plaintext)

        iv = cipher.iv
        encrypted_payload = iv + ciphered_data

        encoded_encrypted_payload = b64encode(encrypted_payload).decode(ENCODING_STANDARD)

        create_table_item(data, encrypted_payload)

        return jsonify({'encrypted_data': encoded_encrypted_payload})

    except Exception as e:
        return jsonify(error=str(e)), 500


def decrypt(data):
    try:
        record_id = data.get('id')
        item_type = data.get('itemType')

        encrypted_data = retrieve_item_by_id(record_id, item_type)

        password = get_secret(ENCRYPT_DECRYPT_PASSWORD_SECRET_NAME)
        salt = get_secret(ENCRYPT_DECRYPT_SALT_SECRET_NAME)

        key = PBKDF2(password, salt, dkLen=32)

        iv = encrypted_data[:16]
        encrypted_data = encrypted_data[16:]

        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        decrypted_data = cipher.decrypt(encrypted_data)
        unpadded_data = unpad(decrypted_data, AES.block_size)

        return unpadded_data.decode(ENCODING_STANDARD)
    except Exception as e:
        return jsonify(error=str(e)), 500
