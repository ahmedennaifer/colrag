import os
import logging

from io import BytesIO
from typing import Union, Dict, Any

from botocore.exceptions import ClientError
import boto3
from fastapi import UploadFile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class S3Wrapper:
    """
    Simple wrapper around the boto3 S3 API, for basic operations.
    """

    def __init__(self, endpoint: str = None) -> None:
        self.resource = "s3"
        self.client = boto3.client(
            "s3",
            region_name=os.environ.get("AWS_DEFAULT_REGION"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )

    def ensure_bucket_exists(self, bucket_name: str) -> None:
        try:
            self.client.head_bucket(Bucket=bucket_name)
        except ClientError:
            self.create_bucket(bucket_name)


    def create_bucket(self, bucket_name: str) -> None:
        self.client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': os.environ.get('AWS_DEFAULT_REGION')
            }
        )
        logger.info(f"Created bucket {bucket_name}")


    def get_client(self) -> "boto3.Client":
        logger.debug("Getting client...")
        return self.client

    def get_s3_object(
        self, bucket_name: str, key: str, get_raw: bool = False
    ) -> Union[BytesIO, Dict[str, Any]]:
        """
        gets s3 object from bucket name and key.
        :param bucket_name: name of the bucket to get object from.
        :param key: key of the object to get.
        :param get_raw: whether to return Bytes object or full response data.
        """
        if get_raw:
            try:
                logger.debug("Getting raw object...")
                return self.client.get_object(Bucket=bucket_name, Key=key)
            except ClientError as e:
                logger.error(f"Could not get object from {bucket_name}/{key}: {e}")
        try:
            byte_object = self.client.get_object(Bucket=bucket_name, Key=key)
            logger.info(f"Got object from {bucket_name}/{key}: {byte_object['Body']}")
            return BytesIO(byte_object["Body"].read())
        except ClientError as e:
            logger.error(f"Could not get object from {bucket_name}/{key}: {e}")

    def upload_file(self, file: UploadFile, bucket: str, key: str) -> None:
        """
        Uploads file to s3 bucket.
        """
        try:
            file.file.seek(0)  # Reset file pointer to beginning
            self.client.upload_fileobj(
                file.file,
                bucket,
                key
            )
            try:
                self.client.head_object(Bucket=bucket, Key=key)
                logger.info(f"Successfully verified upload of {key} to {bucket}")
            except ClientError:
                raise Exception(f"File upload failed verification for {key}")

        except ClientError as e:
            logger.error(f"Could not upload file to {bucket}/{key}: {e}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error uploading file: {e}")
            raise e
