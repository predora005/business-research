# coding: utf-8

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

##############################
# 指定した複数銘柄の株価を取得する
##############################
def get_stock_prices(codes, start_year, end_year):
    """ 指定した複数銘柄の株価を取得する。
    
    Args:
        codes       (dict)  : 証券コードと名称のディクショナリ
                                 (ex){'JR東日本':9020, 'JR西日本': 9021}
        start_year  (int)   : 取得開始年
        end_year    (int)   : 取得終了年
    Returns:
        DataFrame   : 取得した情報を格納したDataFrame
    """
    
    whole_df = None
    for name in codes.keys():
        
        # 指定した証券コードの決算情報を取得する。
        code = codes[name]
        df = get_stock_price(code, start_year, end_year)
        
        # 株価情報のデータタイプを修正する
        df = astype_stock_price(df)
        
        # 株価情報に移動平均を追加する
        df = add_moving_average_stock_price(df)
        
        # 銘柄名を追加し、MultiIndexにする。
        df['銘柄'] = name
        df = df.set_index('銘柄', append=True)
        
        if whole_df is None:
            whole_df = df
        else:
            whole_df = whole_df.append(df)
        
        # 1秒ディレイ
        time.sleep(1)
    
    # indexを入れ替える
    whole_df = whole_df.swaplevel('銘柄', '日付').sort_index()
    
    return whole_df
    
##############################
# 指定した銘柄の株価を取得する
##############################
def get_stock_price(code, start_year, end_year):
    """ 指定した銘柄の株価を取得する。
    
    Args:
        code        (int)   : 証券コード
        start_year  (int)   : 取得開始年
        end_year    (int)   : 取得終了年
        
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

##################################################
# 複数銘柄の株価を折れ線グラフで可視化する
##################################################
def visualize_multi_stock_prices_in_line(df, brand_names, show_average=False, filepath=None):
    """ 複数銘柄の株価を折れ線グラフで可視化する
    
    Args:
        df          (DataFrame) : 複数銘柄の株価が格納されたデータフレーム
        brand_names (list)      : 可視化する銘柄名のリスト
        filepath    (string)    : 可視化したグラフを保存するファイルパス
    
    Returns:
    """
    # 銘柄数
    brand_num = len(brand_names)
    
    # figsize, rows, colsを取得
    figsize, rows, cols = get_subplot_size(brand_num)
    
    # Figureを取得
    fig = plt.figure(figsize=figsize)

    # 銘柄別に折れ線グラフで表示する
    for i in range(brand_num):
        
        # Axesを取得
        ax = fig.add_subplot(rows, cols, i+1)
        
        # 銘柄名
        brand_name = brand_names[i]
        
        # 表示するデータを抽出
        df_brand = df.loc[brand_name,]
        x = df_brand.index  # 日付
        y = df_brand['終値']
        
        # 折れ線グラフ表示
        label = '{0:s}-終値'.format(brand_name)
        ax.plot(x, y, label=label, linewidth=2.0)
        
        # 移動平均の折れ線グラフを追加
        if show_average:
            average_columns = ['5日移動平均', '25日移動平均', '75日移動平均']
            for column in average_columns:
                x = df_brand.index      # 日付
                y = df_brand[column]    # 移動平均
                label = '{0:s}-{1:s}'.format(brand_name, column)
                ax.plot(x, y, label=label, linewidth=1.0)
        
        # 目盛り線を表示
        ax.grid(color='gray', linestyle='--', linewidth=0.5)
        
        # 軸ラベルをセット
        #plt.xlabel(data_name, size=15)
        
        # 凡例を表示
        #ax.legend(brand_names)
        ax.legend()
        
        # グラフのタイトルを追加
        ax.set_title(brand_name)
        
        # Y軸の表示範囲を設定
        #if from_zero:
        #    ax.set_ylim(ymin=0)
    
    # 不要な余白を削る
    plt.tight_layout()
    
    # グラフを表示
    fig.show()
    
    # グラフをファイルに出力
    if filepath is not None:
        fig.savefig(filepath)
        
        
##################################################
# 複数グラフ表示する際の各種サイズを返す
##################################################
def get_subplot_size(plot_num):
    """ 複数グラフ表示する際の各種サイズを返す
    
    Args:
        plot_num     (int)  : 表示するグラフの個数

    Returns:
        figsize, rows, cols (int)
    """
    
    # サブプロットの行数・列数を決定
    if plot_num == 1:
        rows, cols = (1, 1)
        figsize=(6, 4)
    elif plot_num == 2:
        rows, cols = (1, 2)
        figsize=(10, 4)
    elif plot_num == 3:
        rows, cols = (1, 3)
        figsize=(15, 4)
    elif plot_num == 4:
        rows, cols = (2, 2)
        figsize=(10, 8)
    elif plot_num <= 6:
        rows, cols = (2, 3)
        figsize=(15, 8)
    elif plot_num <= 9:
        rows, cols = (3, 3)
        figsize=(15, 12)
    else:
        rows, cols = (4, 4)
        figsize=(20, 16)
        
        
    return figsize, rows, cols