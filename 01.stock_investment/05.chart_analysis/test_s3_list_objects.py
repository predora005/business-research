# coding: utf-8

import boto3

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    BUCKET_NAME = ''
    
    """
    # 全オブジェクト表示(Resource)
    print('==============================')
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    objects = bucket.objects.all()
    for obj in objects:
        print(obj.key)
        #print(obj)
        
    # 全オブジェクト表示(Client)
    print('==============================')
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)
    for obj in response['Contents']:
        print(obj['Key'])
        #print(obj)
    
    # Prefixで指定したオブジェクト表示(Resource)
    print('==============================')
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    objects = bucket.objects.filter(Prefix='dir1/')
    for obj in objects:
        print(obj.key)
        #print(obj)
    
    # Prefixで指定したオブジェクト表示(Client)
    print('==============================')
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix='dir2/')
    for obj in response['Contents']:
        print(obj['Key'])
        #print(obj)
    
    # バケット直下のオブジェクト表示(Resource)
    print('==============================')
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    objects = bucket.objects.filter(Delimiter='/')
    for obj in objects:
        print(obj.key)

    # バケット直下のオブジェクト表示(Client)
    print('==============================')
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Delimiter='/')
    for obj in response['Contents']:
        print(obj['Key'])
    """
    
    # Keyが1,000件以上ある場合の模擬(Resource)
    print('==============================')
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    marker = ''
    while  True:
        # オブジェクト取得
        objects = bucket.objects.filter(Marker=marker, MaxKeys=5)
        
        # オブジェクト表示
        last_key = None
        for obj in objects:
            print(obj.key)
            last_key = obj.key
        
        # 最後のキーをMarkerにセットし次のオブジェクト取得を行う。
        # オブジェクト取得が完了していたら終了。
        if last_key is None:
            break
        else:
            marker = last_key
        
    # Keyが1,000件以上ある場合の模擬(Client)
    print('==============================')
    s3 = boto3.client('s3')
    
    # オブジェクト取得
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, MaxKeys=5)
    while True:
        # オブジェクト表示
        for obj in response['Contents']:
            print(obj['Key'])
        
        # 'NextContinuationToken'が存在する場合は、次のデータ取得。
        if 'NextContinuationToken' in response:
            token = response['NextContinuationToken']
            response = s3.list_objects_v2(Bucket=BUCKET_NAME, MaxKeys=5, ContinuationToken=token)
        else:
            break
        
