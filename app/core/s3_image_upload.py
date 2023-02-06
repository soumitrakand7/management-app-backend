import boto3
from botocore.exceptions import NoCredentialsError
from .config import settings
import logging
import os
from base64 import b64decode

log = logging.getLogger(__name__)


def upload_to_s3_bucket(image, bucket, s3_file_name):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_S3_ACCESS_KEY,
        aws_secret_access_key=settings.AWS_S3_SECRET_KEY,
    )
    file_name = "./static/temp/" + s3_file_name
    try:
        with open(file_name, "wb+") as f:
            f.write(b64decode(image))
            f.close()
        s3_client.upload_file(file_name, bucket, s3_file_name, ExtraArgs={
            "ContentType": "image/jpeg"})
        log.info("File " + s3_file_name + " uploaded to bucket " + bucket)
        return "https://" + bucket + ".s3.ap-south-1.amazonaws.com/" + s3_file_name
    except FileNotFoundError:
        log.error("File upload failed")
    except NoCredentialsError:
        log.error("Invalid Credentials")
    finally:
        os.remove(file_name)
