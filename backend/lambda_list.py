import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('cloudstore-files')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super().default(obj)

def lambda_handler(event, context):
    try:
        try:
            user_id = event['requestContext']['authorizer']['claims']['sub']
        except:
            user_id = event['requestContext']['authorizer']['sub']

        params = event.get('queryStringParameters') or {}
        folder = params.get('folder', None)

        if folder:
            response = table.query(
                IndexName='userId-folder-index',
                KeyConditionExpression=Key('userId').eq(user_id) & Key('folder').eq(folder)
            )
        else:
            response = table.query(
                KeyConditionExpression=Key('userId').eq(user_id)
            )
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*'},
            'body': json.dumps({'files': response['Items']}, cls=DecimalEncoder)
        }
    except Exception as e:
        return {'statusCode': 500, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'error': str(e)})}