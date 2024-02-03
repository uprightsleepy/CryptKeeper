import boto3
from botocore.exceptions import BotoCoreError, ClientError
from app.config.constants import AWS_REGION, S3_BUCKET_NAME

s3 = boto3.client(
    service_name='s3',
    region_name=AWS_REGION
)


def upload_file(file_path, object_name=None):
    if object_name is None:
        object_name = file_path

    try:
        s3.upload_file(Filename=file_path, Bucket=S3_BUCKET_NAME, Key=object_name)
        print(f"File {file_path} uploaded to {S3_BUCKET_NAME}/{object_name}")
        return True
    except (BotoCoreError, ClientError) as e:
        print(f"Failed to upload {file_path} to {S3_BUCKET_NAME}/{object_name}: {e}")
        return False


def upload_bytes(content, object_name):
    try:
        s3.put_object(Bucket=S3_BUCKET_NAME, Key=object_name, Body=content)
        print(f"Content uploaded to {S3_BUCKET_NAME}/{object_name}")
        return True
    except (BotoCoreError, ClientError) as e:
        print(f"Failed to upload to {S3_BUCKET_NAME}/{object_name}: {e}")
        return False


def download_file(object_name):
    full_object_name = object_name if object_name.startswith('encrypted/') else f"encrypted/{object_name}"

    try:
        response = s3.get_object(Bucket=S3_BUCKET_NAME, Key=full_object_name)
        return response['Body'].read()
    except (BotoCoreError, ClientError) as e:
        print(f"Failed to download {full_object_name} from {S3_BUCKET_NAME}: {e}")
        return None


def list_files():
    try:
        response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME)
        if 'Contents' in response:
            for obj in response['Contents']:
                print(obj['Key'])
        else:
            print(f"No files found in {S3_BUCKET_NAME}")
    except (BotoCoreError, ClientError) as e:
        print(f"Failed to list files in {S3_BUCKET_NAME}: {e}")
