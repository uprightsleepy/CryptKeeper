import boto3
from botocore.exceptions import BotoCoreError, ClientError
from app.config.constants import AWS_REGION, DYNAMODB_TABLE_NAME

dynamodb = boto3.client(
    service_name='dynamodb',
    region_name=AWS_REGION
)


def create_table_item(data, encrypted_payload):
    try:
        table_name = DYNAMODB_TABLE_NAME
        record_id = data.get('id')
        item_type = data.get('itemType')

        item = {
            'RecordID': {'S': record_id},
            'ItemType': {'S': item_type},
            'Data': {'B': encrypted_payload},
        }

        condition = "attribute_not_exists(RecordID) AND attribute_not_exists(ItemType)"

        dynamodb.put_item(TableName=table_name, Item=item, ConditionExpression=condition)
    except (BotoCoreError, ClientError) as e:
        raise Exception("Failed to store item in DynamoDB: " + str(e))


def retrieve_item_by_id(item_id, item_type):
    try:
        table_name = DYNAMODB_TABLE_NAME

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
    except (BotoCoreError, ClientError) as e:
        raise Exception("Failed to retrieve item from DynamoDB: " + str(e))
