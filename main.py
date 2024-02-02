from flask import Flask, request, jsonify
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad
import boto3
import base64

app = Flask(__name__)

client = boto3.client(
    service_name='secretsmanager',
    region_name='us-east-2'
)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    plaintext = request.get_json().get('plaintext')
    password = get_secret('encrypt_decrypt_password')

    salt = get_secret('encrypt_decrypt_salt')

    key = PBKDF2(password, salt, dkLen=32)

    cipher = AES.new(key, AES.MODE_CBC)

    padded_plaintext = pad(plaintext.encode('utf-8'), AES.block_size)
    ciphered_data = cipher.encrypt(padded_plaintext)

    return jsonify({'encrypted_data': ciphered_data.hex()})

def get_secret(secret_name):
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except Exception as e:
        raise e
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return secret
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            return decoded_binary_secret


if __name__ == '__main__':
    app.run(debug=True)
