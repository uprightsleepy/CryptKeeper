# CryptKeeper

CryptKeeper is a secure data storage application that provides robust AES encryption for sensitive information before safely storing it in an AWS DynamoDB table. Designed to ensure data privacy and integrity, CryptKeeper uniquely stores each piece of data to prevent overwriting, making it an ideal solution for managing encrypted payloads. Additionally, it integrates with AWS S3 for encrypted file storage, further enhancing its capability to secure various data types.

## Features

- **Secure Encryption**: Utilizes AES encryption to securely encrypt both textual data and files before storage.
- **DynamoDB Integration**: Seamlessly stores encrypted textual data in DynamoDB with unique keys to prevent data overwriting.
- **S3 Integration**: Efficiently manages encrypted file storage in an S3 bucket, allowing for secure file uploads and downloads.
- **High Data Integrity**: Ensures that each piece of data, whether text or file, is stored uniquely, maintaining the highest levels of data integrity and security.
- **AWS Secrets Manager Integration**: Leverages AWS Secrets Manager for secure management of encryption keys and salts, ensuring that encryption practices meet best security standards.

### Prerequisites

- AWS Account
- Python 3.x
- Boto3 Library
- Access to AWS DynamoDB and necessary permissions
- Access to AWS S3 and necessary permissions
- AWS Secrets Manager for managing encryption secrets

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourrepository/cryptkeeper.git
    cd cryptkeeper
    ```

2. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

   This will install all necessary Python libraries, including Flask, Boto3, and PyCryptodome.

3. **Configure AWS Credentials**:

   Ensure your AWS credentials are set up correctly. These can be configured using the AWS CLI with `aws configure` or by setting environment variables.

4. **Set Environment Variables**:

   Make sure to set up the following environment variables according to your AWS setup:
    - `AWS_REGION`: Your AWS region.
    - `DYNAMODB_TABLE_NAME`: The name of your DynamoDB table for storing encrypted data.
    - `S3_BUCKET_NAME`: The name of your S3 bucket for storing encrypted files.
    - Secrets for encryption/decryption stored in AWS Secrets Manager.

## Usage

The application exposes a Flask-based web API with endpoints for encrypting and decrypting data, as well as uploading and downloading encrypted files. Here are some key endpoints:

- **Encrypt Text**: `POST /encrypt` with JSON containing the data to encrypt.
- **Decrypt Text**: `POST /decrypt` with JSON specifying the data to decrypt.
- **Upload Encrypted File**: `POST /encrypt-file` with the file to be encrypted and uploaded.
- **Download Decrypted File**: `POST /decrypt-file` with the filename to decrypt and download.

For detailed API usage, please refer to the included Postman collection or Swagger documentation.

## Contact
For support or inquiries, please contact [Henry Phillips](mailto:henry@designedbyhenryp.com).
