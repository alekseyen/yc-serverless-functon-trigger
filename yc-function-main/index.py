import os
import datetime
import boto3
import pytz

ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")
TIME_ZONE = os.getenv("TIME_ZONE", "Europe/Moscow")

TEMP_FILENAME = "/tmp/temp_file"
TEXT_FOR_TEMP_FILE = "This is text file"

def write_temp_file():
    temp_file = open(TEMP_FILENAME, 'w')
    temp_file.write(TEXT_FOR_TEMP_FILE)
    temp_file.close()
    print("\U0001f680 Temp file is written")

def get_now_datetime_str():
    now = datetime.datetime.now(pytz.timezone(TIME_ZONE))    
    return now.strftime('%Y-%m-%d__%H-%M-%S')

def get_s3_instance():
    session = boto3.session.Session()
    return session.client(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net'
    )

def upload_dump_to_s3():
    print("\U0001F4C2 Starting upload to Object Storage")
    get_s3_instance().upload_file(
        Filename=TEMP_FILENAME,
        Bucket=BUCKET_NAME,
        Key=f'file-{get_now_datetime_str()}.txt'
    )
    print("\U0001f680 Uploaded")


def remove_temp_files():
    os.remove(TEMP_FILENAME)
    print("\U0001F44D That's all!")

def handler(event, context):
    write_temp_file()
    upload_dump_to_s3()
    remove_temp_files()
    return {
        'statusCode': 200,
        'body': 'File is uploaded',
    }

