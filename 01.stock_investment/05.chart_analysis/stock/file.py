# coding: utf-8

import pandas as pd
import os

##############################
# 指定した銘柄コードの株価保存ファイルの名称を取得する
##############################
def get_stock_prices_filename(dirpath, code):
    
    filename = code + '.pkl'
    filepath = os.path.join(dirpath, filename)
    
    return filepath
    
##############################
# 指定した銘柄コードの株価チャートのファイル名称を取得する
##############################
def get_chart_filename(dirpath, code):
    
    filename = f'{code}.png'
    filepath = os.path.join(dirpath, filename)
    
    return filepath
    
##############################
# テクニカル指標分析のファイル名称を取得する
##############################
def get_tech_analyze_filename(dirpath):
    
    filename = 'tech_analyze.csv'
    filepath = os.path.join(dirpath, filename)
    
    return filepath
    
##############################
# 指定した銘柄コードの株価保存ファイルの存在有無を確認する
##############################
def isfile_stock_prices(dirpath, code):
    
    filepath = get_stock_prices_filename(dirpath, code)
    exist_file = os.path.isfile(filepath)
    return exist_file

##############################
# 指定した銘柄コードの株価保存ファイルを読み込む
##############################
def read_stock_prices(dirpath, code):

    filepath = get_stock_prices_filename(dirpath, code)
    df = pd.read_pickle(filepath)
    return df
    
##############################
# 指定した銘柄コードの株価保存ファイルを保存する
##############################
def save_stock_prices(dirpath, code, df):
    
    os.makedirs(dirpath, exist_ok=True)
    
    filepath = get_stock_prices_filename(dirpath, code)
    df.to_pickle(filepath)
