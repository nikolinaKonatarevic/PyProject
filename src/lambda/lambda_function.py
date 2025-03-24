import os
from urllib.parse import unquote_plus

import boto3
from PIL import Image


class S3Client:
    def __init__(self):
        self.client = boto3.client("s3")

    def upload(self, file_name:str,download_path: str, new_path: str) -> str:

        file = self.download(file_name, download_path,new_path)
        self.client.upload_fileobj(file, os.environ['BUCKET_NAME'], f'{new_path}/{file_name}')

        url = (
            f"https://{os.environ['BUCKET_NAME']}.s3"
            f".{os.environ['DEFAULT_REGION']}.amazonaws.com/{new_path}/{file_name}"
        )
        return url

    def download(self, file_name: str, file_path: str, download_path: str):
        result = self.client.download_file(
            Bucket=os.environ["BUCKET_NAME"], Key=f"{file_path}/{file_name}", Filename= download_path)
        return result

    def delete(self, file_name: str, file_path: str) -> None:
        self.client.delete_object(Bucket=os.environ["BUCKET_NAME"], Key=f"{file_path}/{file_name}")


def lambda_handler(event, context):
    s3_client = S3Client()
    for record in event["Records"]:
        key = unquote_plus(record["s3"]["object"]["key"])

        [file_path, file_name] = key.split("/")

        tempfile = f"/tmp/{file_name}"
        s3_client.download(file_name, file_path, download_path=tempfile)

        s3_client.delete(file_name, file_path)
        with Image.open(tempfile) as img:
            img.thumbnail((400, 400))

            img.save(tempfile)
        s3_client.upload(record, "proccessed")
