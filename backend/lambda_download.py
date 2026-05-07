import json
import boto3
from decimal import Decimal

s3 = boto3.client('s3', region_name='ap-south-1')
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('cloudstore-files')
BUCKET_NAME = 'cloudstore-files-yourname'

def lambda_handler(event, context):
    try:
        try:
            user_id = event['requestContext']['authorizer']['claims']['sub']
        except:
            user_id = event['requestContext']['authorizer']['sub']

        file_id = event['pathParameters']['fileId']
        response = table.get_item(Key={'userId': user_id, 'fileId': file_id})
        item = response.get('Item')
        if not item:
            return {'statusCode': 404, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'error': 'File not found'})}

        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': item['s3Key']},
            ExpiresIn=300
        )
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*'},
            'body': json.dumps({'downloadUrl': presigned_url})
        }
    except Exception as e:
        return {'statusCode': 500, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'error': str(e)})}