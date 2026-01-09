import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('vehicle-dashbord')

response = table.query(
    KeyConditionExpression=Key('vehicle_id').eq('8f3c2b4e-9d12-4a7f-8c3e-52b1f6a9d7c4'),
    ScanIndexForward=False,  # 降順（新しい順）
    Limit=1                  # 1件だけ取得
)

latest_item = response['Items'][0]
print(latest_item)
