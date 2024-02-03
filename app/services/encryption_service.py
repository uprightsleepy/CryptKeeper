from base64 import b64encode

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad

from flask import jsonify

from app.config.constants import ENCODING_STANDARD
from app.data.dynamodb_access import create_table_item, retrieve_item_by_id
from app.utils.secrets_manager import get_secrets


def encrypt_data(plaintext, password, salt):
    key = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_CBC)
    padded_plaintext = pad(plaintext.encode(ENCODING_STANDARD), AES.block_size)
    ciphered_data = cipher.encrypt(padded_plaintext)
    iv = cipher.iv
    return iv + ciphered_data


def encrypt(data):
    try:
        plaintext = data.get('plaintext')
        password, salt = get_secrets()
        encrypted_payload = encrypt_data(plaintext, password, salt)
        encoded_encrypted_payload = b64encode(encrypted_payload).decode(ENCODING_STANDARD)
        create_table_item(data, encrypted_payload)
        return jsonify({'encrypted_data': encoded_encrypted_payload})
    except Exception as e:
        return jsonify(error=str(e)), 500


def decrypt_data(encrypted_data, password, salt):
    key = derive_key(password, salt)
    iv = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_data = cipher.decrypt(encrypted_data)
    return unpad(decrypted_data, AES.block_size)


def decrypt(data):
    try:
        record_id = data.get('id')
        item_type = data.get('itemType')
        encrypted_data = retrieve_item_by_id(record_id, item_type)
        password, salt = get_secrets()
        unpadded_data = decrypt_data(encrypted_data, password, salt)
        return unpadded_data.decode(ENCODING_STANDARD)
    except Exception as e:
        return jsonify(error=str(e)), 500


def derive_key(password, salt):
    return PBKDF2(password, salt, dkLen=32)
