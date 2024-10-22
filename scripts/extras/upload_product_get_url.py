import boto3
import os
import pandas as pd
from mimetypes import MimeTypes
from botocore.exceptions import NoCredentialsError
import re

# Define the regex pattern
pattern = re.compile(r'^[A-Z0-9]+_[A-Za-z\s-]+_\d+\.(jpg|png)$')

# https://us-east-1.console.aws.amazon.com/s3/buckets/ecomm-milano-images?region=us-east-1&bucketType=general&tab=objects

# AWS Credentials
ACCESS_KEY = ""
SECRET_KEY = ''
BUCKET_NAME = 'ecomm-milano-images'
FOLDER_PATH = 'images/upload_new_1'
CSV_FILE_PATH = "data/upload_new_1_s3_url_images.csv"


# Function to get MIME type based on file extension
def get_mime_type(file_path):
    mime = MimeTypes()
    mime_type, _ = mime.guess_type(file_path)
    return mime_type

# Function to rename file extension to .jpg


def rename_file_to_jpg(file_path):
    base, _ = os.path.splitext(file_path)
    new_file_path = base + '.jpg'
    os.rename(file_path, new_file_path)
    return new_file_path


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        content_type = get_mime_type(local_file) or 'application/octet-stream'
        s3.upload_file(local_file, bucket, s3_file, ExtraArgs={
                       'ContentType': content_type, 'ACL': 'public-read'})
        url = f"https://{bucket}.s3.amazonaws.com/{s3_file}"
        # print(f'Successfully uploaded {local_file} to {
        #       bucket}/{s3_file} with Content-Type {content_type}')
        return url

    except FileNotFoundError:
        print(f'The file {local_file} was not found')
        return False
    except NoCredentialsError:
        print('Credentials not available')
        return False


# Function to upload images and save URLs to CSV
def upload_images_and_save_urls(folder_path, bucket_name, csv_file_path):
    image_data = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # if not bool(pattern.match(file)):
            #     print(file)
            #     break
            # else:
            #     print("good")

            if file.endswith(('jpg', 'jpeg', 'png', 'gif')):

                # Add more file types if needed
                local_file_path = os.path.join(root, file)
                new_file_path = rename_file_to_jpg(local_file_path)
                # Maintain directory structure in the S3 bucket
                s3_file_path = os.path.relpath(new_file_path, folder_path)
                url = upload_to_aws(new_file_path, bucket_name, s3_file_path)
                if url:
                    image_data.append(
                        {'product_name': os.path.basename(new_file_path), 'Product Code': file.split("_")[0], 'url': url})

    # Save the image data to a CSV file
    df = pd.DataFrame(image_data)
    df.to_csv(csv_file_path, index=False)
    print(f'Successfully saved image data to {csv_file_path}')


if __name__ == '__main__':
    upload_images_and_save_urls(FOLDER_PATH, BUCKET_NAME, CSV_FILE_PATH)
