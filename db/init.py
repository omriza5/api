import boto3
from botocore.exceptions import ClientError

boto3.setup_default_session(profile_name="terraform")
dynamodb = boto3.resource("dynamodb",region_name = "us-west-2")

try:   
    table = dynamodb.create_table(
        TableName="pokemons",
        KeySchema=[
            {"AttributeName": "id", "KeyType": "HASH"},  # Primary partition key
        ],
        AttributeDefinitions=[
            {"AttributeName": "id", "AttributeType": "S"},
            {"AttributeName": "name", "AttributeType": "S"},  # Attribute for GSI
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "name-index",
                "KeySchema": [{"AttributeName": "name", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5,
                },
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5,
        }
    )

    print("Creating Database...")
    table.meta.client.get_waiter("table_exists").wait(TableName="pokemons")
    print("Table created successfully.")
except ClientError as e:
    print(f"Failed to create table: {e.response['Error']['Message']}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
    