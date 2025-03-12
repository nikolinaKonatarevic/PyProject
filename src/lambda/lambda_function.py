from urllib.parse import unquote_plus

import boto3
from fastapi import UploadFile
from PIL.Image import Image

from src.api.config import settings


class S3Client:
    def __init__(self):
        self.client = boto3.client("s3")

    def upload(self, doc: UploadFile, file_path: str) -> str:
        self.client.upload_fileobj(doc.file, settings.AWS_BUCKET_NAME, f"{file_path}/{doc.filename}")

        url = (
            f"https://{settings.AWS_BUCKET_NAME}.s3"
            f".{settings.AWS_DEFAULT_REGION}.amazonaws.com/{file_path}/{doc.filename}"
        )
        return url

    def download(self, file_name: str, file_path: str, download_path: str):
        # result = self.client.get_object(Bucket=settings.AWS_BUCKET_NAME, Key=f"{file_path}/{file_name}")
        result = self.client.download_file(
            Bucket=settings.AWS_BUCKET_NAME, Key=f"{file_path}/{file_name}", FileName=download_path
        )
        return result

    def delete(self, file_name: str, file_path: str) -> None:
        self.client.delete_object(Bucket=settings.AWS_BUCKET_NAME, Key=f"{file_path}/{file_name}")


s3_client = S3Client()


def lambda_handler(event, context):
    for record in event["Records"]:
        # bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])

        # Extracting file_path and file_name from the key
        [file_path, file_name] = key.split("/")

        tempfile = f"/tmp/{file_name}"
        s3_client.download(file_name, file_path, tempfile)

        s3_client.delete(file_name, file_path)
        # crop the quality - pillow quality;

        with Image.open(tempfile) as img:
            img.thumbnail((400, 400))

            img.save(tempfile)
        # In db I store path to the proccessed folder, not unproccessed
        # Upload the document to the destination bucket (this example uploads to a new bucket with '-documents' suffix)

        s3_client.upload(record, "processed")
