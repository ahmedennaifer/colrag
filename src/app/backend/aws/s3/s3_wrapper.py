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
        self.endpoint = endpoint if endpoint else os.environ["LOCALSTACK_ENDPOINT"]
        self.resource = "s3"
        self.client = boto3.client(self.resource, endpoint_url=self.endpoint)

    def create_bucket(self, bucket_name: str) -> None:
        self.client.create_bucket(Bucket=bucket_name)
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
        Uploads file to s3 bucket. Pretty simple :D
        :param file: fastAPI UploadFile.
        :param bucket: name of the bucket to upload to.
        :param key: key of the object to upload.
        """
        try:
            logger.debug(f"Uploading file from {file.filename} to {bucket}/{key}...")
            self.client.upload_fileobj(file.file, bucket, key)
            logger.info(f"Uploaded file from {bucket}/{key} to {bucket}/{key}...")

        except ClientError as e:
            logger.error(f"Could not upload file to {bucket}/{key}: {e}")
            # client.put_object(f, cle, buffer)
