import os
import boto3
import uuid


def upload(self, image) -> str:
    # connect to boto3
    service_name = "s3"
    endpoint_url = "https://kr.object.ncloudstorage.com"
    access_key = os.getenv("NCP_ACCESS_KEY")
    secret_key = os.getenv("NCP_SECRET_KEY")
    s3 = boto3.client(
        service_name,
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    bucket_name = "follow-image"
    image_id = f"{str(uuid.uuid4())}.{image.name.split('.')[-1]}"
    s3.upload_fileobj(image.file, bucket_name, image_id)
    s3.put_object_acl(Bucket=bucket_name, Key=image_id, ACL="public-read")
    url = f"{endpoint_url}/{bucket_name}/{image_id}"
    return url
