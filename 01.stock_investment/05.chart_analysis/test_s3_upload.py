# coding: utf-8

import logging
import boto3
from botocore.exceptions import ClientError

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    BUCKET_NAME = ''
    OBJECT_NAME1 = 'dir3/file1.txt'
    FILE_NAME1 = 'file1.txt'
    OBJECT_NAME2 = 'dir3/file2.txt'
    FILE_NAME2 = 'file2.txt'
    OBJECT_NAME3 = 'dir3/file3.csv'
    FILE_NAME3 = 'file3.csv'
    OBJECT_NAME4 = 'dir3/file4.txt'
    FILE_NAME4 = 'file4.txt'
    
    #upload_file(FILE_NAME1, BUCKET_NAME, object_name=None)
    #upload_file(FILE_NAME1, BUCKET_NAME, OBJECT_NAME1)
    
    
    s3 = boto3.resource('s3')
    s3.Bucket(BUCKET_NAME).upload_file(FILE_NAME1, OBJECT_NAME1)
    
    s3  = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    with open(FILE_NAME2, 'rb') as f:
        bucket.upload_fileobj(f, OBJECT_NAME2)
    
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(FILE_NAME3, BUCKET_NAME, OBJECT_NAME3)
    
    s3 = boto3.client('s3')
    with open(FILE_NAME4, 'rb') as f:
        s3.upload_fileobj(f, BUCKET_NAME, OBJECT_NAME4)