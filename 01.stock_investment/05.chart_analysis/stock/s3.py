# coding: utf-8

import boto3
import datetime
from stock.file import *

##############################
# 指定した銘柄コードの株価保存ファイルをS3からダウンロードする
##############################
def s3_download_stock_prices(dirpath, code):
    
    # バケット名を取得
    bucket_name = __get_bucket_name()
    
    # S3上での株価保存ファイルのオブジェクト名を取得
    object_name = __get_stock_prices_object_name(code)
    
    # S3にオブジェクトが存在するか確認
    obj_exists = __object_exists(bucket_name, object_name)
    
    # オブジェクトが存在する場合はダウンロード
    if obj_exists:
        # ダウンロード先のファイル名を取得
        file_name = get_stock_prices_filename(dirpath, code)
        
        # S3からダウンロード
        __download(bucket_name, object_name, file_name)
        
    return obj_exists
    
##############################
# 指定した銘柄コードの株価保存ファイルをS3にアップロードする
##############################
def s3_upload_stock_prices(dirpath, code):
    
    # バケット名を取得
    bucket_name = __get_bucket_name()
    
    # ローカルのファイル名を取得
    file_name = get_stock_prices_filename(dirpath, code)
    
    # S3上での株価保存ファイルのオブジェクト名を取得
    object_name = __get_stock_prices_object_name(code)
    
    # S3にアップロード
    __upload(bucket_name, file_name, object_name)
    
##############################
# 指定した銘柄コードの株価チャートをS3にアップロードする
##############################
def s3_upload_chart(dirpath, code):
    
    # バケット名を取得
    bucket_name = __get_bucket_name()
    
    # ローカルのファイル名を取得
    file_name = get_chart_filename(dirpath, code)
    
    # S3上での株価保存ファイルのオブジェクト名を取得
    object_name = __get_chart_object_name(code)
    
    # S3にアップロード
    __upload(bucket_name, file_name, object_name)
    
##############################
# テクニカル指標分析結果をS3にアップロードする
##############################
def s3_upload_analysis(dirpath):
    
    # バケット名を取得
    bucket_name = __get_bucket_name()
    
    # ローカルのファイル名を取得
    file_name = get_tech_analyze_filename(dirpath)
    
    # S3上でのテクニカル指標分析結果ファイルのオブジェクト名を取得
    object_name = __get_analysis_object_name()
    
    # S3にアップロード
    __upload(bucket_name, file_name, object_name)
    
##############################
# 指定した銘柄コードの株価保存ファイルについて、
# S3上でのオブジェクト名を取得する
##############################
def __get_stock_prices_object_name(code):
    
    obj_name = f'prices/{code}.pkl'
    
    return obj_name
    
##############################
# 指定した銘柄コードの株価チャートファイルについて、
# S3上でのオブジェクト名を取得する
##############################
def __get_chart_object_name(code):
    
    # ファイル名
    filename = f'{code}.png'
    
    # ディレクトリ名は日付とする
    now_date = datetime.datetime.now()
    dirname = now_date.strftime('%04Y%02m%02d')
    
    obj_name = f'{dirname}/chart/{filename}'
    
    return obj_name
    
##############################
# テクニカル指標分析結果ファイルについて、
# S3上でのオブジェクト名を取得する
##############################
def __get_analysis_object_name():
    
    # ファイル名
    filename = 'tech_analyze.csv'
    
    # ディレクトリ名は日付とする
    now_date = datetime.datetime.now()
    dirname = now_date.strftime('%04Y%02m%02d')
    
    obj_name = f'{dirname}/{filename}'
    
    return obj_name
    
##############################
# S3に指定したオブジェクトが存在するか確認する
##############################
def __object_exists(bucket_name, object_name):
    
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    objects = bucket.objects.filter(Prefix=object_name)
    
    obj_exists = False
    for obj in objects:
        obj_exists = True
        
    return obj_exists
    
##############################
# S3からダウンロードする
##############################
def __download(bucket_name, object_name, file_name):
    
    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).download_file(object_name, file_name)
    
##############################
# S3にアップロードする
##############################
def __upload(bucket_name, file_name, object_name):
    
    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).upload_file(file_name, object_name)
    
##############################
# S3のバケット名を取得する
##############################
def __get_bucket_name():
    
    return ''
    
