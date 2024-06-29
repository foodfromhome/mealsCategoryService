import os
from pydantic import BaseConfig
from dotenv import load_dotenv

load_dotenv()


class GlobalConfig(BaseConfig):
    s3_access_key = os.getenv("S3_ACCESS_KEY")
    s3_secret_key = os.getenv("S3_SECRET_KEY")
    s3_bucket_name = os.getenv("S3_BUCKET_NAME")
    s3_endpoint_url = os.getenv("S3_ENDPOINT_URL")
    s3_access_id = os.getenv("S3_ACCESS_ID")

    mongo_username = os.getenv("DB_USERNAME")
    mongo_password = os.getenv("DB_PASSWORD")
    mongo_host = os.getenv("DB_HOST")
    mongo_port = os.getenv("DB_PORT")
    mongo_db = os.getenv("DB_NAME")

    redis_host = os.getenv("REDIS_SERVER")
    redis_port = os.getenv("REDIS_PORT")


settings = GlobalConfig()
