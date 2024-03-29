import boto3
import base64
from app.config.constants import AWS_REGION, ENCRYPT_DECRYPT_PASSWORD_SECRET_NAME, ENCRYPT_DECRYPT_SALT_SECRET_NAME

secrets_manager = boto3.client(
    service_name='secretsmanager',
    region_name=AWS_REGION
)


def get_secret(secret_name):
    try:
        get_secret_value_response = secrets_manager.get_secret_value(
            SecretId=secret_name
        )
    except Exception as e:
        raise e
    else:
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            return decoded_binary_secret


def get_secrets():
    password = get_secret(ENCRYPT_DECRYPT_PASSWORD_SECRET_NAME)
    salt = get_secret(ENCRYPT_DECRYPT_SALT_SECRET_NAME)
    return password, salt
