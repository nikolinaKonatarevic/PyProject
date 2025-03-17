import os
from urllib.parse import unquote_plus

import boto3
from PIL.Image import Image


class S3Client:
    def __init__(self):
        self.client = boto3.client("s3")

    def upload(self, doc, file_path: str) -> str:
        self.client.upload_fileobj(doc.file, os.environ["AWS_BUCKET_NAME"], f"{file_path}/{doc.filename}")

        url = (
            f"https://{os.environ['AWS_BUCKET_NAME']}.s3"
            f".{os.environ['AWS_DEFAULT_REGION']}.amazonaws.com/{file_path}/{doc.filename}"
        )
        return url

    def download(self, file_name: str, file_path: str, download_path: str):
        result = self.client.download_file(
            Bucket=os.environ["AWS_BUCKET_NAME"], Key=f"{file_path}/{file_name}", FileName=download_path
        )
        return result

    def delete(self, file_name: str, file_path: str) -> None:
        self.client.delete_object(Bucket=os.environ["AWS_BUCKET_NAME"], Key=f"{file_path}/{file_name}")


def lambda_handler(event, context):
    s3_client = S3Client()
    for record in event["Records"]:
        key = unquote_plus(record["s3"]["object"]["key"])

        [file_path, file_name] = key.split("/")

        tempfile = f"/tmp/{file_name}"
        s3_client.download(file_name, file_path, tempfile)

        s3_client.delete(file_name, file_path)
        with Image.open(tempfile) as img:
            img.thumbnail((400, 400))

            img.save(tempfile)
        s3_client.upload(record, "processed")
