# coding: utf-8

import mplfinance as mpf
from stock.techind import *

##################################################
# 株価チャートを表示する その１
##################################################
def show_stock_chart1(df, figname=None):
    
    # 日付で昇順ソース
    df_sort = df.sort_index()
    
    # ローソク足チャートを表示
    mpf.plot(df_sort, type='candle', mav=(5, 25 ,75), volume=True, savefig=figname)
    
##################################################
# 株価チャートを表示する その2
##################################################
def show_stock_chart2(df, title='', figpath=None):
    
    # 日付で昇順ソース
    df_sort = df.sort_index()
    
    # MACDを追加
    df_macd = add_macd(df_sort)
    print('==========')
    print(df_macd)
    
    # MACDとシグナルのプロット作成
    add_plot = [mpf.make_addplot(df_macd['MACD'], color='m', panel=1, secondary_y=False),
        mpf.make_addplot(df_macd['Signal'], color='c', panel=1, secondary_y=False),
        mpf.make_addplot(df_macd['Hist'], type='bar', color='g', panel=1, secondary_y=True)]
    
    # ローソク足チャートを表示
    mpf.plot(df_sort, type='candle',
        mav=(5, 25 ,75), volume=True, addplot=add_plot, volume_panel=2, savefig=figpath)
    
##################################################
# 株価チャートを表示する その3
##################################################
def show_stock_chart3(df, title='', figpath=None):
    
    # 日付で昇順ソース
    df_sort = df.sort_index()
    
    # MACDを追加
    df_macd = add_macd(df_sort)

    # RSIを追加
    df_rsi = add_rsi(df_macd)
    print('==========')
    print(df_rsi)
    
    # MACDとRSIのプロット作成
    add_plot = [mpf.make_addplot(df_rsi['MACD'], color='m', panel=1, secondary_y=False),
        mpf.make_addplot(df_rsi['Signal'], color='c', panel=1, secondary_y=False),
        mpf.make_addplot(df_rsi['Hist'], type='bar', color='g', panel=1, secondary_y=True),
        mpf.make_addplot(df_rsi['RSI'], panel=2)]
    
    # ローソク足チャートを表示
    mpf.plot(df_rsi, type='candle',
        mav=(5, 25 ,75), volume=True, addplot=add_plot, volume_panel=3, savefig=figpath)
    
##################################################
# 株価チャートを表示する その4
##################################################
def show_stock_chart4(df, title='', figpath=None):
    
    # 日付で昇順ソース
    df_sort = df.sort_index()
    
    # MACDを追加
    df_macd = add_macd(df_sort)
    
    # RSIを追加
    df_rsi = add_rsi(df_macd)
    print('==========')
    print(df_rsi)
    
    # MACDとRSIのプロット作成
    add_plot = [mpf.make_addplot(df_rsi['MACD'], color='m', panel=1, secondary_y=False),
        mpf.make_addplot(df_rsi['Signal'], color='c', panel=1, secondary_y=False, ylabel='MACD'),
        mpf.make_addplot(df_rsi['Hist'], type='bar', color='g', panel=1, secondary_y=True, ylabel='Hist'),
        mpf.make_addplot(df_rsi['RSI'], panel=2, ylabel='RSI')]
    
    # ローソク足チャートを表示
    mpf.plot(df_rsi, type='candle',
        mav=(5, 25 ,75), volume=True, addplot=add_plot, volume_panel=3, 
        title=title, figratio=(5, 4), panel_ratios=(6, 3, 3, 2),
        style='nightclouds', savefig=figpath)
    
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