# CryptKeeper

CryptKeeper is an advanced data encryption and secure storage solution that leverages AES encryption to protect sensitive information. It seamlessly integrates with AWS DynamoDB and S3 for robust storage capabilities, and employs AWS Lambda for automated file processing, ensuring data privacy, integrity, and efficient management of different data types.

## Features

- **AES Encryption**: Implements top-tier AES encryption for text and file data, securing it before storage.
- **DynamoDB Integration**: Securely stores encrypted text data in DynamoDB, using unique keys for each item to avoid data overwriting and ensure integrity.
- **S3 and Lambda Integration**: Manages encrypted file storage in S3 buckets, with Lambda functions automating the file processing workflow for secure uploads, transitions, and downloads.
- **AWS Secrets Manager**: Utilizes AWS Secrets Manager for the secure handling of encryption keys and salts, maintaining adherence to the highest security standards.
- **Enhanced Data Security**: Ensures the highest levels of security and integrity for all stored data, backed by AWS’s reliable infrastructure.

### Prerequisites

- An active AWS Account
- Python 3.x
- Boto3 and other necessary Python libraries
- Properly configured access to AWS DynamoDB, S3, and Lambda with appropriate permissions
- AWS Secrets Manager for managing encryption secrets

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourrepository/cryptkeeper.git
    cd cryptkeeper
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
   This will install Flask, Boto3, PyCryptodome, and other required libraries.

3. **Configure AWS Credentials**:
   Setup your AWS credentials for programmatic access via the AWS CLI (`aws configure`) or by setting environment variables.

4. **Environment Variable Setup**:
   Configure the following environment variables according to your AWS setup:
   - `AWS_REGION`: The AWS region of operation.
   - `DYNAMODB_TABLE_NAME`: The name of your DynamoDB table for encrypted text storage.
   - `S3_BUCKET_NAME`: The name of your S3 bucket for encrypted file storage.
   - Encryption keys and salts managed through AWS Secrets Manager.

## Usage

CryptKeeper offers a Flask-based API for encryption and decryption operations, including file handling:
- **Encrypt Text**: `POST /encrypt` with the plaintext data.
- **Decrypt Text**: `POST /decrypt` with the id of the encrypted data.
- **Upload Encrypted File**: `POST /encrypt-file` for file encryption and subsequent upload.
- **Download Decrypted File**: `POST /decrypt-file` for downloading and decrypting files.

For detailed API usage, refer to the included Postman collection or Swagger documentation.

## Contact

For support or inquiries, please contact [Henry Phillips](mailto:henry@designedbyhenryp.com).
