import boto3
import os
from dotenv import load_dotenv

load_dotenv()
 
aws_access_key_id = os.environ.get('aws_access_key_id')
aws_secret_access_key = os.environ.get('aws_secret_access_key')
aws_session_token= os.environ.get('aws_session_token')

# s3 = boto3.client('s3',
#                     aws_access_key_id,
#                     aws_secret_access_key,
#                     aws_session_token
#                     )
# BUCKET_NAME='lats-image-data'

def upload_file(file_name, bucket):
    object_name = file_name
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)
    return response

def list_files(bucket):
    s3 = boto3.client('s3')
    contents = []
    try:
        for item in s3.list_objects(Bucket=bucket)['Contents']:
            # print(item)
            contents.append(item)
    except Exception as e:
        pass

    return contents

def show_image(bucket):
    s3 = boto3.client('s3')
    location = boto3.client('s3').get_bucket_location(Bucket=bucket)['LocationConstraint']
    print("[DATA] : location = ", location)
    public_urls = []
    try:
        for item in s3.list_objects(Bucket=bucket)['Contents']:
            print(item['Key'])
            url = "https://s3-{}.amazonaws.com/{}/{}".format(location, bucket, item['Key'])
            presigned_url = s3.generate_presigned_url('get_object', Params = {'Bucket': bucket, 'Key': item['Key']}, ExpiresIn = 100)
            print("[DATA] : presigned url = ", presigned_url)
            public_urls.append(presigned_url)
    except Exception as e:
        pass
    print("[DATA] : The contents inside show_image = ", public_urls)
    return public_urls
    
    
    
    