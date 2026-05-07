import json
import boto3
import secrets
from datetime import datetime, timezone, timedelta

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
files_table = dynamodb.Table('cloudstore-files')
links_table = dynamodb.Table('cloudstore-shared-links')

def lambda_handler(event, context):
    try:
        try:
            user_id = event['requestContext']['authorizer']['claims']['sub']
        except:
            user_id = event['requestContext']['authorizer']['sub']

        file_id = event['pathParameters']['fileId']
        response = files_table.get_item(Key={'userId': user_id, 'fileId': file_id})
        item = response.get('Item')
        if not item:
            return {'statusCode': 404, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'error': 'File not found'})}

        share_token = secrets.token_urlsafe(16)
        expires_at  = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()

        links_table.put_item(Item={
            'shareToken': share_token, 'userId': user_id,
            'fileId': file_id, 's3Key': item['s3Key'],
            'fileName': item['fileName'], 'expiresAt': expires_at,
            'createdAt': datetime.now(timezone.utc).isoformat()
        })
        files_table.update_item(
            Key={'userId': user_id, 'fileId': file_id},
            UpdateExpression='SET isShared = :val',
            ExpressionAttributeValues={':val': True}
        )
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*'},
            'body': json.dumps({'shareToken': share_token, 'expiresAt': expires_at})
        }
    except Exception as e:
        return {'statusCode': 500, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'error': str(e)})}