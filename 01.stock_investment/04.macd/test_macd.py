# coding: utf-8

from pltinit import *
from stock import *
import pandas as pd
import datetime
import os

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    #  matplotlibの日本語フォント設定処理
    plt_font_init()
    
    # 銘柄コード
    code = '9020.JP'
    
    # 指定した銘柄コードの株価を読み込む
    dirpath = os.getcwd()
    filename = code + '.pickle'
    filepath = os.path.join(dirpath, filename)
    exist_file = os.path.isfile(filepath)
    
    if exist_file:
        stored_df = pd.read_pickle(filepath)
        print('==========')
        print(stored_df)
        
        latest_date = stored_df.index.max()
        print('==========')
        print(latest_date)
        
        start_date = latest_date + datetime.timedelta(days=1)
        end_date = start_date + datetime.timedelta(days=1)
        
    else:
        # ファイルが無い場合は、直近5日間の株価を取得する
        stored_df = None
        #end_date = datetime.datetime.now()
        end_date = datetime.datetime(2021, 3, 1)
        start_date = end_date + datetime.timedelta(days=-1)
    
    # 指定した銘柄コードの株価を取得する
    df = get_stock_prices(code, start_date, end_date)
    print('==========')
    print(df)
    
    # 既存のデータと新たに取得したデータを結合する
    if stored_df is None:
        new_stored_df = df
    else:
        new_stored_df = pd.concat([df, stored_df])
    print('==========')
    print(new_stored_df)
        
        
    # 株価をファイルに保存する
    new_stored_df.to_pickle(filepath)
