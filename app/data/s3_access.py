import boto3
from botocore.exceptions import BotoCoreError, ClientError
from app.config.constants import AWS_REGION

s3 = boto3.client(
    service_name='s3',
    region_name=AWS_REGION
)


def upload_file(file_path, bucket_name, object_name=None):
    if object_name is None:
        object_name = file_path

    try:
        s3.upload_file(Filename=file_path, Bucket=bucket_name, Key=object_name)
        print(f"File {file_path} uploaded to {bucket_name}/{object_name}")
        return True
    except (BotoCoreError, ClientError) as e:
        print(f"Failed to upload {file_path} to {bucket_name}/{object_name}: {e}")
        return False


def upload_bytes(content, bucket_name, object_name):
    try:
        s3.put_object(Bucket=bucket_name, Key=object_name, Body=content)
        print(f"Content uploaded to {bucket_name}/{object_name}")
        return True
    except (BotoCoreError, ClientError) as e:
        print(f"Failed to upload to {bucket_name}/{object_name}: {e}")
        return False


def download_file(bucket_name, object_name):
    full_object_name = object_name if object_name.startswith('encrypted/') else f"encrypted/{object_name}"

    try:
        response = s3.get_object(Bucket=bucket_name, Key=full_object_name)
        return response['Body'].read()
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchKey':
            raise FileNotFoundError(f"The object {full_object_name} does not exist in bucket {bucket_name}.") from e
        else:
            print(f"Failed to download {full_object_name} from {bucket_name}: {e}")
            return None
    except BotoCoreError as e:
        print(f"An error occurred: {e}")
        return None

