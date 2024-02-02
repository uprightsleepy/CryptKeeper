import boto3

dynamodb = boto3.client(
    service_name='dynamodb',
    region_name='us-east-2'
)


def create_table_item(data, encrypted_payload):
    table_name = "EncryptionDataTable"
    record_id = data.get('id')
    item_type = data.get('itemType')

    item = {
        'RecordID': {'S': record_id},
        'ItemType': {'S': item_type},
        'Data': {'B': encrypted_payload},
    }

    try:
        dynamodb.put_item(TableName=table_name, Item=item)
    except Exception as e:
        print(f"Error storing item in DynamoDB: {e}")


def retrieve_item_by_id(item_id, item_type):
    table_name = "EncryptionDataTable"

    response = dynamodb.get_item(
        TableName=table_name,
        Key={
            'RecordID': {'S': item_id},
            'ItemType': {'S': item_type}
        }
    )

    item = response.get('Item', {})
    encrypted_data = item.get('Data', {}).get('B', b'')
    return encrypted_data
