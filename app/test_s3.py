import boto3


s3_client = boto3.client(
    service_name='s3',
    region_name='us-west-2',
    aws_access_key_id='XXXX',
    aws_secret_access_key='XXXXX'
)

# Print out bucket names
# for bucket in s3_client.buckets.all():
#     print(bucket.name)

def upload_file( bucket_name , file_path , object_name):
    try:
        s3_client.upload_file(file_path , bucket_name ,object_name)
        return True
    except Exception as e:
        print(e)
        return False
    
def download_file( bucket_name , file_path , object_name):
    try:
        s3_client.download_file( bucket_name ,object_name,file_path)
        return True
    except Exception as e:
        print(e)
        return False
    
def delete_file(bucket_name , file_name):
    try:
        s3_client.delete_object(Bucket= bucket_name , Key=file_name)
        return True
    except Exception as e:
        print(e)
        return False
