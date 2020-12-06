# coding: utf-8

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

##############################
# 指定した銘柄の株価を取得する
##############################
def get_stock_price(code, start_year, end_year):
    """ 指定した銘柄の決算情報を取得する。
    
    Args:
        code    (int) : 証券コード

    Returns:
        DataFrame  : 決算情報を格納したDataFrame
    """
    
    whole_df = None
    headers = None
    
    # 指定した年数分の株価を取得する
    years = range(start_year, end_year+1)
    for year in years:
        
        # 指定URLのHTMLデータを取得
        url = 'https://kabuoji3.com/stock/{0:d}/{1:d}/'.format(code, year)
        html_headers ={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        html = requests.get(url, headers=html_headers)
        
        # BeautifulSoupのHTMLパーサーを生成
        bs = BeautifulSoup(html.content, "html.parser")
        
        # <table>要素を取得
        table = bs.find('table')

        # <table>要素内のヘッダ情報を取得する。
        if headers is None:
            headers = []
            thead_th = table.find('thead').find_all('th')
            for th in thead_th:
                headers.append(th.text)
        
        # <tr>要素のデータを取得する。
        rows = []
        tr_all = table.find_all('tr')
        for i, tr in enumerate(tr_all):
            
            # 最初の行は<thead>要素なので飛ばす
            if i==0:
                continue
            
            # <tr>要素内の<td>要素を取得する。
            row = []
            td_all = tr.find_all('td')
            for td in td_all:
                row.append(td.text)
            
            # 1行のデータをリストに追加
            rows.append(row)
            
        # DataFrameを生成する
        df = pd.DataFrame(rows, columns=headers)
        
        # DataFrameを結合する
        if whole_df is None:
            whole_df = df
        else:
            whole_df = pd.concat([whole_df, df])
        
        # 1秒ディレイ
        time.sleep(1)
    
    return whole_df
    
##################################################
# 株価情報のデータタイプを修正する
##################################################
def astype_stock_price(df):
    """ 株価情報のデータタイプを修正する
    
    Args:
        df          (DataFrame) : 株価が格納されたデータフレーム

    Returns:
        DataFrame  : データタイプ修正後のDataFrame
    """
    
    dtypes = {}
    
    for column in df.columns:
        if column == '日付':
            dtypes[column] = 'datetime64'
        else:
            dtypes[column] ='float64'
            
    # データ型を変換
    new_df = df.astype(dtypes)
    
    # インデックスを日付に変更
    new_df = new_df.set_index('日付')
    
    return new_df

##################################################
# 株価情報に移動平均を追加する
##################################################
def add_moving_average_stock_price(df):
    """ 株価情報に移動平均を追加する
    
    Args:
        df          (DataFrame) : 株価が格納されたデータフレーム

    Returns:
        DataFrame  : データ追加後のDataFrame
    """
    
    df['5日移動平均'] = df['終値'].rolling(window=5).mean()
    df['25日移動平均'] = df['終値'].rolling(window=25).mean()
    df['75日移動平均'] = df['終値'].rolling(window=75).mean()
    
    return df
    
##################################################
# 株価を折れ線グラフで可視化する
##################################################
def visualize_stock_price_in_line(df, title=None, show_average=False, filepath=None):
    """ 決算情報のうち指定した複数データを折れ線グラフで可視化する
    
    Args:
        df              (DataFrame) : 株価が格納されたデータフレーム
        show_average    (boolean)   : 移動平均を表示するか否か
        filepath        (string)    : 可視化したグラフを保存するファイルパス
    
    Returns:
    """
    
    # FigureとAxesを取得
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    
    # 終値の折れ線グラフを追加
    x = df.index
    y = df['終値']
    ax.plot(x, y, label='終値', linewidth=2.0)
    
    # 移動平均の折れ線グラフを追加
    if show_average:
        average_columns = ['5日移動平均', '25日移動平均', '75日移動平均']
        for column in average_columns:
            x = df.index
            y = df[column]
            ax.plot(x, y, label=column, linewidth=1.0)
    
    # 目盛り線を表示
    ax.grid(color='gray', linestyle='--', linewidth=0.5)
    
    # 凡例を表示
    ax.legend()
    
    # グラフのタイトルを追加
    if title is not None:
        ax.set_title(title)
    
    # グラフを表示
    fig.show()
    
    # グラフをファイルに出力
    if filepath is not None:
        fig.savefig(filepath)    
