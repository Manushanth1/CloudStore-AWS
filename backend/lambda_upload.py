import json
import boto3
from datetime import datetime, timezone

s3 = boto3.client('s3', region_name='ap-south-1')
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('cloudstore-files')
BUCKET_NAME = 'cloudstore-files-yourname'

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        from decimal import Decimal
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super().default(obj)

def lambda_handler(event, context):
    try:
        raw_body = event.get('body') or '{}'
        body = json.loads(raw_body)
        try:
            user_id = event['requestContext']['authorizer']['claims']['sub']
        except:
            user_id = event['requestContext']['authorizer']['sub']

        file_name = body.get('fileName', 'unnamed')
        file_type = body.get('fileType', 'application/octet-stream')
        folder    = body.get('folder', 'root')
        file_size = int(body.get('fileSize', 0))
        file_id   = f"file_{int(datetime.now().timestamp())}_{file_name}"
        s3_key    = f"uploads/{user_id}/{file_id}"

        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': BUCKET_NAME, 'Key': s3_key, 'ContentType': file_type},
            ExpiresIn=300
        )
        table.put_item(Item={
            'userId': user_id, 'fileId': file_id,
            'fileName': file_name, 'fileSize': file_size,
            'fileType': file_type, 'folder': folder,
            's3Key': s3_key,
            'uploadedAt': datetime.now(timezone.utc).isoformat(),
            'isShared': False
        })
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*'},
            'body': json.dumps({'uploadUrl': presigned_url, 'fileId': file_id, 's3Key': s3_key})
        }
    except Exception as e:
        return {'statusCode': 500, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'error': str(e)})}