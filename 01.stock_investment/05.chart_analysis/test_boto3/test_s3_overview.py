# coding: utf-8

import boto3

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    BUCKET_NAME = ''
    
    # 全バケットを表示
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        print(bucket.name)
    
    # バケット内の全オブジェクトを表示
    bucket = s3.Bucket(BUCKET_NAME)
    objects = bucket.objects.all()
    for obj in objects:
        print(obj.key)
        
    # オブジェクトをダウンロード
    s3.Bucket(BUCKET_NAME).download_file('input/file.txt', 'file.txt')
    
    # オブジェクトをアップロード
    s3.Bucket(BUCKET_NAME).upload_file('file.txt', 'output/file.txt')
    
    # オブジェクトを削除
    s3.Object(BUCKET_NAME, 'output/file.txt').delete()
    
    