# coding: utf-8

import pandas as pd
import mplfinance as mpf
from stock.macd import *

##################################################
# 株価チャートを表示する その１
##################################################
def show_stock_chart1(df, figname=None):
    
    # 日付で昇順ソース
    df_sort = df.sort_index()
    
    # ロウソク足チャートを表示
    mpf.plot(df_sort, type='candle', mav=(5, 25 ,75), volume=True, savefig=figname)
    
##################################################
# 株価チャートを表示する その2
##################################################
def show_stock_chart2(df, title='', figname=None):
    
    # 日付で昇順ソース
    df_sort = df.sort_index()
    
    # MACDを追加
    df_macd = add_macd(df_sort)
    print('==========')
    print(df_macd)
    
    # MACDとシグナルのプロット作成
    add_plot = [mpf.make_addplot(df_macd['MACD'], color='r', panel=1, secondary_y=False),
        mpf.make_addplot(df_macd['Signal'], color='b', panel=1, secondary_y=False),
        mpf.make_addplot(df_macd['Hist'], type='bar', color='g', panel=1, secondary_y=True)]
    
    # ロウソク足チャートを表示
    mpf.plot(df_sort, type='candle',
        mav=(5, 25 ,75), volume=True, addplot=add_plot, volume_panel=2, 
        savefig=figname)
    
##################################################
# 株価チャートを表示する その3
##################################################
def show_stock_chart3(df, title='', figname=None):
    
    # 日付で昇順ソース
    df_sort = df.sort_index()
    
    # MACDを追加
    df_macd = add_macd(df_sort)
    print('==========')
    print(df_macd)
    
    # MACDとシグナルのプロット作成
    add_plot = [mpf.make_addplot(df_macd['MACD'], color='r', panel=1, secondary_y=False),
        mpf.make_addplot(df_macd['Signal'], color='b', panel=1, secondary_y=False),
        mpf.make_addplot(df_macd['Hist'], type='bar', color='g', panel=1, secondary_y=True)]
    
    # ロウソク足チャートを表示
    mpf.plot(df_sort, type='candle',
        mav=(5, 25 ,75), volume=True, addplot=add_plot, volume_panel=2, 
        title=title, figratio=(3, 2), panel_ratios=(6, 3, 2),
        style='nightclouds', savefig=figname)
    
##################################################
# 終値の移動平均を追加する
##################################################
def add_sma(df):
    """ 終値の移動平均を追加する
    
    Args:
        df          (DataFrame) : 株価が格納されたデータフレーム
    Returns:
        DataFrame  : データ追加後のDataFrame
    """
    
    df['SMA5'] = df['終値'].rolling(window=5).mean()
    df['SMA25'] = df['終値'].rolling(window=25).mean()
    df['SMA75'] = df['終値'].rolling(window=75).mean()
    
    return df