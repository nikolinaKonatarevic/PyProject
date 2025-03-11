import boto3
from fastapi import UploadFile

from src.config import settings


class S3Client:
    def __init__(self):
        self.client = boto3.client("s3")

    def upload(self, doc: UploadFile, project_id: int, file_path: str) -> str:
        self.client.upload_fileobj(doc.file, settings.AWS_BUCKET_NAME, f"{file_path}/{doc.filename}")

        url = (
            f"https://{settings.AWS_BUCKET_NAME}.s3"
            f".{settings.AWS_DEFAULT_REGION}.amazonaws.com/{file_path}/{doc.filename}"
        )
        return url

    def download(self, file_name: str, file_path: str):
        result = self.client.get_object(Bucket=settings.AWS_BUCKET_NAME, Key=f"{file_path}/{file_name}")
        return result

    def delete(self, file_name: str, file_path: str) -> None:
        self.client.delete_object(Bucket=settings.AWS_BUCKET_NAME, Key=f"{file_path}/{file_name}")
