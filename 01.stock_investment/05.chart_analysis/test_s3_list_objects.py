# coding: utf-8

import boto3

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    BUCKET_NAME = ''
    
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    objects = bucket.objects.all()
    for obj in objects:
        print(obj.key)
        
    