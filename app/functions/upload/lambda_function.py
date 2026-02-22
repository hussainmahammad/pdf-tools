import boto3
import json
import uuid
import os

s3 = boto3.client('s3')
BUCKET = os.environ['BUCKET_NAME']

HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
}

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        filename = body.get("filename")

        # If filename provided → use it
        if filename:
            key = f"uploads/{filename}"
        else:
            key = f"uploads/{uuid.uuid4()}.pdf"

        url = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': BUCKET,
                'Key': key,
                'ContentType': 'application/pdf'
            },
            ExpiresIn=300
        )

        return {
            "statusCode": 200,
            "headers": HEADERS,
            "body": json.dumps({
                "upload_url": url,
                "file_key": key
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": HEADERS,
            "body": json.dumps({"error": str(e)})
        }
