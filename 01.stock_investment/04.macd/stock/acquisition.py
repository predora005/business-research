# coding: utf-8

import pandas_datareader.data as web
from stock.file import *
import datetime

##############################
# 指定した銘柄コードの株価を取得する
##############################
def get_stock_prices(code, start_date, end_date=None):

    # 指定銘柄コードの株価を取得する
    stock_prices = web.DataReader(code, 'stooq', start=start_date, end=end_date)
        
    return stock_prices
    
##################################################
# 指定銘柄コードの株価を取得・更新する
##################################################
def update_stock_prices(dirpath, code, start_date=None, end_date=None):
    
    # ファイルの存在有無を取得する
    exist_file = isfile_stock_prices(dirpath, code)
    
    ##################################################
    # ファイルが存在する場合
    ##################################################
    if exist_file:
        # ファイルが存在すれば読み込む
        stored_df = read_stock_prices(dirpath, code)
        print('==========')
        print(stored_df)
        
        # 保存されたデータの期間を取得する
        latest_date = stored_df.index.max()
        oldest_date = stored_df.index.min()
        
        # 開始・終了日付の妥当性をチェックし補正して返す
        start_date, end_date = __check_start_end_date(start_date, end_date, oldest_date, latest_date)
        print('==========')
        print(start_date, end_date)
        
        # 指定した銘柄コードの株価を取得する
        if (start_date < oldest_date) and (latest_date < end_date):
            # 指定した期間が、保存データの期間を内包する場合
            df1 = get_stock_prices(code, start_date, oldest_date + datetime.timedelta(days=-1))
            df2 = get_stock_prices(code, latest_date + datetime.timedelta(days=1), end_date)
            new_stored_df = pd.concat([df2, stored_df, df1])
        else:
            df = get_stock_prices(code, start_date, end_date)
            if end_date < oldest_date:
                new_stored_df = pd.concat([stored_df, df])
            else:
                new_stored_df = pd.concat([df, stored_df])
                
        # 株価をファイルに保存する
        save_stock_prices(dirpath, code, new_stored_df)
        
        return new_stored_df
    
    ##################################################
    # ファイルが存在しない場合
    ##################################################
    else:
        if (start_date is None) and (end_date is None):
            # 期間の指定が無い場合は、直近5日間とする
            end_date = datetime.datetime.now()
            start_date = end_date + datetime.timedelta(days=-4)
        
        elif (start_date is None) and (end_date is not None):
            # end_dateを含む5日間とする
            start_date = end_date + datetime.timedelta(days=-4)
        
        elif (start_date is not None) and (end_date is None):
            # start_date以降の全期間とする
            pass
        
        # 指定した銘柄コードの株価を取得する
        df = get_stock_prices(code, start_date, end_date)
        
        # 株価をファイルに保存する
        save_stock_prices(dirpath, code, df)
        
        return df
        
##################################################
# 開始・終了日付の妥当性をチェックし補正して返す
##################################################
def __check_start_end_date(start_date, end_date, oldest_date, latest_date):
    
   # 開始日付がNone
   if start_date is None:
       # 保存された日付以降の株価を取得する
       start_date = latest_date + datetime.timedelta(days=1)
   
   # 終了日付がNone
   if end_date is None:
       # 本日日付までの株価を取得する
       end_date = datetime.datetime.now()
   
   # 日付を補正する
   if oldest_date <= start_date <= latest_date:
       start_date = latest_date + datetime.timedelta(days=1)
   if oldest_date <= end_date <= latest_date:
       end_date = oldest_date + datetime.timedelta(days=-1)
       
   # 日付の整合性をチェックする
   if start_date > end_date:
       raise Exception('Invalid start_date > end_date')
   
   return start_date, end_date
   