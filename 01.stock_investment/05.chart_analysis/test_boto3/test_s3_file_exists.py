# coding: utf-8

import boto3

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    BUCKET_NAME = ''
    filename = '9020.JP/9020.JP.pkl'
    
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    objects = bucket.objects.filter(Prefix=filename)
    print(objects)
    print(vars(objects))
    
    file_exists = False
    for obj in objects:
        file_exists = True
        
    print(file_exists)
