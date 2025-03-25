import os
from urllib.parse import unquote_plus

import boto3
from PIL import Image


class S3Client:
    def __init__(self):
        self.client = boto3.client("s3")

    def upload(self, file_name:str,download_path: str, new_path: str) -> str:
        print(f"in the upload - {file_name} +++ {download_path} +++ {new_path}")

        self.download(file_name, download_path,new_path)

        self.client.upload_file(f"{download_path}/{file_name}", os.environ['BUCKET_NAME'], f'{new_path}/{file_name}')


    def download(self, file_name: str, file_path: str, download_path: str):
        print (f"download {file_path}  +++  {file_name} ++ {download_path}")
        # Get object from S3
        response = self.client.get_object(
            Bucket=os.environ["BUCKET_NAME"],
            Key=f"{file_path}/{file_name}"
        )

        # Read file content and save it locally
        with open(download_path, "wb") as f:
            f.write(response["Body"].read())

        print("Download complete.")


    def delete(self, file_name: str, file_path: str) -> None:
        print("in the delete ")
        self.client.delete_object(Bucket=os.environ["BUCKET_NAME"], Key=f"{file_path}/{file_name}")
        print("delete ended ")


def lambda_handler(event, context):
    s3_client = S3Client()
    for record in event["Records"]:
        key = unquote_plus(record["s3"]["object"]["key"])

        [file_path, file_name] = key.split("/")
        print (f"{file_path}  +++  {file_name}")
        tempfile = f"documents/{file_name}"

        s3_client.download(file_name, file_path, download_path=tempfile)

        with Image.open(tempfile) as img:
            img.thumbnail((400, 400))
            print(f"save photo")
            img.save(tempfile)

        print("before last upload")

        s3_client.upload(file_name, "documents", "proccessed")

        s3_client.delete(file_name, file_path)