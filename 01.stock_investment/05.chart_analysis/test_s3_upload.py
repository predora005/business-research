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
    OBJECT_NAME1 = 'test/data_j.csv'
    FILE_NAME1 = 'data_j.csv'
    OBJECT_NAME2 = 'test/PIL3.8.zip'
    FILE_NAME2 = 'PIL3.8.zip'
    OBJECT_NAME3 = 'test/test.txt'
    FILE_NAME3 = 'text.txt'
    
    #upload_file(FILE_NAME1, BUCKET_NAME, object_name=None)
    upload_file(FILE_NAME1, BUCKET_NAME, OBJECT_NAME1)
    
    
    s3 = boto3.resource('s3')
    s3.Bucket('BUCKET_NAME').upload_file(OBJECT_NAME3, FILE_NAME3)
