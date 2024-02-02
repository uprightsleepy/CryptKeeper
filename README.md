# CryptKeeper

CryptKeeper is a secure data storage application that provides robust AES encryption for sensitive 
information before safely storing it in an AWS DynamoDB table. Designed to ensure data privacy and integrity, 
CryptKeeper uniquely stores each piece of data to prevent overwriting, making it an ideal solution for managing encrypted payloads.

## Features

- **Secure Encryption**: Utilizes AES encryption to securely encrypt data before storage.
- **DynamoDB Integration**: Seamlessly stores encrypted data in DynamoDB with unique keys to prevent data overwriting.
- **High Data Integrity**: Ensures that each piece of data is stored uniquely, maintaining the highest levels of data integrity and security.

### Prerequisites

- AWS Account
- Python 3.x
- Boto3 Library
- Access to AWS DynamoDB and necessary permissions
