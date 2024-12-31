import os
from dotenv import load_dotenv
import boto3

load_dotenv()


def test_connection():
    s3 = boto3.client(
        "s3",
        region_name="eu-north-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        buckets = s3.list_buckets()
        print("Buckets:", [b["Name"] for b in buckets["Buckets"]])

        bucket_name = os.getenv("BUCKET_NAME")
        s3.head_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} exists and is accessible")

        objects = s3.list_objects_v2(Bucket=bucket_name)
        if "Contents" in objects:
            print("Objects in bucket:", [obj["Key"] for obj in objects["Contents"]])
        else:
            print("Bucket is empty")

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    test_connection()
