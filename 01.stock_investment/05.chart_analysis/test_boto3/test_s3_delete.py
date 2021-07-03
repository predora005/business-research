# coding: utf-8

import boto3

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    BUCKET_NAME = ''
    OBJECT_NAME1 = 'dir3/file1.txt'
    OBJECT_NAME2 = 'dir3/file2.txt'
    OBJECT_NAME3 = 'dir3/file3.csv'
    OBJECT_NAME4 = 'dir3/file4.txt'
    
    print('==============================')
    s3 = boto3.resource('s3')
    response = s3.Object(BUCKET_NAME, OBJECT_NAME1).delete()
    print(response)
    
    print('==============================')
    s3 = boto3.client('s3')
    response = s3.delete_object(
        Bucket=BUCKET_NAME,
        Key=OBJECT_NAME2,
    )
    print(response)
    
    print('==============================')
    s3  = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    response = bucket.delete_objects(
        Delete={
            'Objects': [
                {'Key': OBJECT_NAME3},
                {'Key': OBJECT_NAME4}
            ]
        },
    )
    print(response)
    
    print('==============================')
    s3 = boto3.client('s3')
    response = s3.delete_objects(
        Bucket=BUCKET_NAME,
        Delete={
            'Objects': [
                {'Key': OBJECT_NAME3},
                {'Key': OBJECT_NAME4}
            ]
        },
    )
    print(response)
