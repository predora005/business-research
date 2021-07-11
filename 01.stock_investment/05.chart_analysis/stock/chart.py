# coding: utf-8

import mplfinance as mpf
from stock.file import *
from stock.techind import *
from stock.s3 import *

##################################################
# 株価チャートを表示・保存する
##################################################
def save_stock_chart(df, dirpath, code):
    
    # 日付で昇順ソース
    df_sort = df.sort_index()
    
    # MACDを追加
    df_macd = add_macd(df_sort)
    
    # RSIを追加
    df_rsi = add_rsi(df_macd)
    print('==========')
    print('[save_stock_chart]')
    print(df_rsi)
    
    # 保存先のファイルパスを作成
    figpath = get_chart_filename(dirpath, code)
    
    # すべてNaNの列が含まれるか確認
    has_nan_column = df_rsi.isnull().all().any()
    
    # NaNの列が含まれる場合は最低限の情報のみ表示
    if has_nan_column:
        save_stock_chart_minimum(df_rsi, figpath, title=code)
    else:
        save_stock_chart_all(df_rsi, figpath, title=code)
    
    # 保存したファイルをS3にアップロードする
    s3_upload_chart(dirpath, code)
    
##################################################
# 株価チャートを表示・保存する(最低限の情報のみ)
##################################################
def save_stock_chart_minimum(df, figpath, title=''):
    
    # ローソク足チャートを表示
    mpf.plot(df, type='candle', 
        mav=(5, 25 ,75), volume=True, 
        title=title, savefig=figpath)
    
##################################################
# 株価チャートを表示・保存する(すべての情報)
##################################################
def save_stock_chart_all(df, figpath, title=''):
    
    # MACDとRSIのプロット作成
    add_plot = [mpf.make_addplot(df['MACD'], color='m', panel=1, secondary_y=False),
        mpf.make_addplot(df['Signal'], color='c', panel=1, secondary_y=False, ylabel='MACD'),
        mpf.make_addplot(df['Hist'], type='bar', color='g', panel=1, secondary_y=True, ylabel='Hist'),
        mpf.make_addplot(df['RSI'], panel=2, ylabel='RSI')]
    
    # ローソク足チャートを表示
    mpf.plot(df, type='candle',
        mav=(5, 25 ,75), volume=True, addplot=add_plot, volume_panel=3, 
        title=title, figratio=(5, 4), panel_ratios=(6, 3, 3, 2),
        style='nightclouds', savefig=figpath)
    