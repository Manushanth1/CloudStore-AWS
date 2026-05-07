import json
import boto3

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

        s3.delete_object(Bucket=BUCKET_NAME, Key=item['s3Key'])
        table.delete_item(Key={'userId': user_id, 'fileId': file_id})
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*'},
            'body': json.dumps({'message': 'File deleted successfully'})
        }
    except Exception as e:
        return {'statusCode': 500, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'error': str(e)})}