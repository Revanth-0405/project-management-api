import boto3

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:8000",
    region_name="us-east-1",
    aws_access_key_id="dummy",
    aws_secret_access_key="dummy"
)

table = dynamodb.create_table(
    TableName="Tasks",
    KeySchema=[
        {"AttributeName": "project_id", "KeyType": "HASH"},
        {"AttributeName": "task_id", "KeyType": "RANGE"}
    ],
    AttributeDefinitions=[
        {"AttributeName": "project_id", "AttributeType": "N"},
        {"AttributeName": "task_id", "AttributeType": "S"}
    ],
    BillingMode="PAY_PER_REQUEST"
)

print("Tasks table created")
