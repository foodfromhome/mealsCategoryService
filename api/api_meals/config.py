from api.s3.main import S3Client
from dotenv import load_dotenv
import os

load_dotenv()

s3_client = S3Client(
    access_key=os.getenv('S3_ACCESS_KEY'),
    secret_key=os.getenv('S3_SECRET_KEY'),
    bucket_name=os.getenv('S3_BUCKET_NAME'),
    endpoint_url=os.getenv('S3_ENDPOINT_URL'),
)
