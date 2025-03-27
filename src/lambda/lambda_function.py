import os
from urllib.parse import unquote_plus

import boto3
from PIL import Image


class S3Client:
    def __init__(self):
        self.client = boto3.client("s3")

    def upload(self, file_name:str, file_path: str, new_path: str):
        self.client.upload_file(f"{file_path}/{file_name}", os.environ['BUCKET_NAME'], f'{new_path}/{file_name}')


    def download(self, file_name: str, file_path: str, new_path: str):
        # Get object from S3
        response = self.client.get_object(
            Bucket=os.environ["BUCKET_NAME"],
            Key=f"{file_path}/{file_name}"
        )

        os.makedirs(os.path.dirname(new_path), exist_ok=True)

        # Read file content and save it locally
        with open(new_path, "wb") as f:
            f.write(response["Body"].read())



    def delete(self, file_name: str, file_path: str) -> None:
        self.client.delete_object(Bucket=os.environ["BUCKET_NAME"], Key=f"{file_path}/{file_name}")


def lambda_handler(event, context):
    s3_client = S3Client()
    for record in event["Records"]:
        key = unquote_plus(record["s3"]["object"]["key"])

        [file_path, file_name] = key.split("/")
        tempfile = f"/tmp/{file_name}"

        s3_client.download(file_name, file_path, new_path=tempfile)

        try:
            with Image.open(tempfile) as img:
                img.thumbnail((400, 400))  # Resize
                img.save(tempfile)  # Overwrite the file with the processed image
        except Exception as e:
            return


        try:
            s3_client.upload(file_name, "/tmp", "proccessed")
        except Exception as e:
            return
        s3_client.delete(file_name, file_path)