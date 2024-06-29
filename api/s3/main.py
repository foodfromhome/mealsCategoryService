from aiobotocore.session import get_session
from contextlib import asynccontextmanager
from fastapi import UploadFile
import uuid
from beanie import PydanticObjectId
from config import settings


class S3Client:
    def __init__(self,
                 access_key: str,
                 secret_key: str,
                 bucket_name: str,
                 endpoint_url: str,
                 access_id: str
                 ):
        self.config = {
            'aws_access_key_id': access_key,
            'aws_secret_access_key': secret_key,
            'endpoint_url': endpoint_url
        }

        self.bucket_name = bucket_name
        self.session = get_session()
        self.access_id = access_id

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client('s3', **self.config) as s3_client:
            yield s3_client

    async def upload_file(self, photo: UploadFile, meal_id: PydanticObjectId, type: str):
        async with self.get_client() as s3_client:
            file_name = f"{type}/{meal_id}/photos/{uuid.uuid4()}-{photo.filename}"
            file_content = await photo.read()

            await s3_client.put_object(Body=file_content, Bucket=self.bucket_name, Key=file_name)

            return f"https://{self.access_id}.storage.msk.3hcloud.com/{self.bucket_name}/{file_name}"


s3_client = S3Client(
    access_key=settings.s3_access_key,
    secret_key=settings.s3_secret_key,
    bucket_name=settings.s3_bucket_name,
    endpoint_url=settings.s3_endpoint_url,
    access_id=settings.s3_access_id
)
