# coding: utf-8

import boto3
import tempfile

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    BUCKET_NAME = ''
    OBJECT_NAME1 = 'dir1/file1.txt'
    FILE_NAME1 = 'file1.txt'
    OBJECT_NAME2 = 'dir1/file2.txt'
    FILE_NAME2 = 'file2.txt'
    OBJECT_NAME3 = 'dir2/file3.csv'
    FILE_NAME3 = 'file3.csv'
    OBJECT_NAME4 = 'dir2/file4.txt'
    FILE_NAME4 = 'file4.txt'
    
    ##############################
    s3 = boto3.resource('s3')
    s3.Bucket(BUCKET_NAME).download_file(OBJECT_NAME1, FILE_NAME1)
    
    ##############################
    # The download_file method
    s3 = boto3.client('s3')
    s3.download_file(BUCKET_NAME, OBJECT_NAME2, FILE_NAME2)
    
    ##############################
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    with open(FILE_NAME3, 'wb') as f:
        bucket.download_fileobj(OBJECT_NAME3, f)
    
    ##############################
    # The download_fileobj method 
    s3 = boto3.client('s3')
    with open(FILE_NAME4, 'wb') as f:
    #with tempfile.NamedTemporaryFile(mode='wb') as f:
        s3.download_fileobj(BUCKET_NAME, OBJECT_NAME4, f)
        print(f.name)
        print(f.tell)
    
    