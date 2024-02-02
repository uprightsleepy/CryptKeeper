from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
from app.data.dynamodb_access import create_table_item, retrieve_item_by_id
from app.utils.secrets_manager import get_secret


def encrypt(data):
    plaintext = data.get('plaintext')
    password = get_secret('encrypt_decrypt_password')
    salt = get_secret('encrypt_decrypt_salt')

    key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_CBC)
    padded_plaintext = pad(plaintext.encode('utf-8'), AES.block_size)
    ciphered_data = cipher.encrypt(padded_plaintext)

    iv = cipher.iv
    encrypted_payload = iv + ciphered_data

    create_table_item(data, encrypted_payload)

    return 'Message has been successfully encrypted.'


def decrypt(data):
    record_id = data.get('id')
    item_type = data.get('itemType')

    encrypted_data = retrieve_item_by_id(record_id, item_type)

    password = get_secret('encrypt_decrypt_password')
    salt = get_secret('encrypt_decrypt_salt')

    key = PBKDF2(password, salt, dkLen = 32)

    iv = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_data = cipher.decrypt(encrypted_data)
    unpadded_data = unpad(decrypted_data, AES.block_size)

    return unpadded_data.decode('utf-8')
