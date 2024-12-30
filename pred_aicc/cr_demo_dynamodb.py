import boto3
import json
from datetime import datetime
from botocore.exceptions import ClientError

# DynamoDB 클라이언트 생성
dynamodb = boto3.client('dynamodb')
table_name = 'CustomerOrders'

def create_table():
    try:
        response = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'customer_id',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'date',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'customer_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'date',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"Table {table_name} created successfully")
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"Table {table_name} already exists")
            return True
        else:
            print(f"Error creating table: {e}")
            return False

def insert_data():
    # 샘플 데이터
    order_data = [
        {"date": "2024-10-01", "type": "Online_Order_Submitted", "customer_id": "S5_20984"},
        {"date": "2024-10-05", "type": "Online_Order_Delivered", "customer_id": "S5_20984"},
        {"date": "2024-10-08", "type": "Online_Order_Return_Initiated", "customer_id": "S5_20984"},
        {"date": "2024-10-11", "type": "Online_Order_Return_Received", "customer_id": "S5_20984"}
    ]
    
    dynamodb_resource = boto3.resource('dynamodb')
    table = dynamodb_resource.Table(table_name)
    
    try:
        with table.batch_writer() as batch:
            for item in order_data:
                batch.put_item(Item=item)
        print("Data inserted successfully")
        return True
    except Exception as e:
        print(f"Error inserting data: {e}")
        return False

def main():
    # 테이블 생성 확인
    if create_table():
        # 테이블이 활성화될 때까지 대기
        waiter = dynamodb.get_waiter('table_exists')
        waiter.wait(TableName=table_name)
        # 데이터 삽입
        insert_data()
    
if __name__ == "__main__":
    main()