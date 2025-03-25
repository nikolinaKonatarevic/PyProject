import os
from urllib.parse import unquote_plus

import boto3
from PIL import Image


class S3Client:
    def __init__(self):
        self.client = boto3.client("s3")

    def upload(self, file_name:str, file_path: str, new_path: str):
        print(f"in the upload - {file_name} +++ {file_path} +++ {new_path}")

        self.download(file_name, file_path, f"{new_path}/{file_name}")

        self.client.upload_file(f"{file_path}/{file_name}", os.environ['BUCKET_NAME'], f'{new_path}/{file_name}')


    def download(self, file_name: str, file_path: str, new_path: str):
        print (f"download {file_path}  +++  {file_name} ++ {new_path}")
        # Get object from S3
        response = self.client.get_object(
            Bucket=os.environ["BUCKET_NAME"],
            Key=f"{file_path}/{file_name}"
        )

        os.makedirs(os.path.dirname(new_path), exist_ok=True)

        # Read file content and save it locally
        with open(new_path, "wb") as f:
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
        tempfile = f"/tmp/{file_name}"

        s3_client.download(file_name, file_path, new_path=tempfile)

        if not os.path.exists(tempfile):
            print(f"File {tempfile} does not exist!")

        try:
            with Image.open(tempfile) as img:
                img.thumbnail((400, 400))  # Resize image
                print(f"Image resized successfully.")
                img.save(tempfile)  # Overwrite the file with the processed image
        except Exception as e:
            print(f"Error processing the image: {e}")
            return

        print("before last upload")

        try:
            s3_client.upload(file_name, "/tmp", "proccessed")
        except Exception as e:
            print(f"Error uploading the file: {e}")
            return
        s3_client.delete(file_name, file_path)