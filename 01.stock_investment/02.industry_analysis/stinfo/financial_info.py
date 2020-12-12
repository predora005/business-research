# coding: utf-8

import requests
from bs4 import BeautifulSoup
import time
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt

##############################
# 指定した複数銘柄の決算情報を取得する
##############################
def get_financial_infos(codes):
    """ 指定した複数銘柄の決算情報を取得する。
    
    Args:
        codes   (dict)  : 証券コードと名称のディクショナリ
                          (ex){'JR東日本':9020, 'JR西日本': 9021}
    Returns:
        DataFrame   : 取得した情報を格納したDataFrame
    """
    
    whole_df = None
    for name in codes.keys():
        
        # 指定した証券コードの決算情報を取得する。
        code = codes[name]
        df = get_financial_info(code)
        
        # 名称を追加し、MultiIndexにする。
        df['名称'] = name
        df = df.set_index('名称', append=True)
        
        if whole_df is None:
            whole_df = df
        else:
            whole_df = whole_df.append(df)
        
        # 1秒ディレイ
        time.sleep(1)
    
    # indexを入れ替える
    whole_df = whole_df.swaplevel('名称', '決算期').sort_index()
    
    return whole_df
    
##############################
# 指定した銘柄の決算情報を取得する
##############################
def get_financial_info(code):
    """ 指定した銘柄の決算情報を取得する。
    
    Args:
        code    (int) : 証券コード

    Returns:
        DataFrame  : 決算情報を格納したDataFrame
    """
    
    # 指定URLのHTMLデータを取得
    url = "https://minkabu.jp/stock/{0:d}/settlement".format(code)
    html = requests.get(url)
    
    # BeautifulSoupのHTMLパーサーを生成
    soup = BeautifulSoup(html.content, "html.parser")
    
    # 決算情報テーブルを取得する
    fin_df1 = get_financial_table(soup, '決算情報')
        
    # 決算情報から不要データを削る。
    fin_df1 = trim_unnecessary_from_dataframe(fin_df1)
        
    # 財務情報テーブルを取得する
    fin_df2 = get_financial_table(soup, '財務情報')
    
    # 財務情報から不要データを削る。
    fin_df2 = trim_unnecessary_from_dataframe(fin_df2)
    
    # キャッシュフロー情報から不要データを削る。
    cf_df = get_cf_table(soup)
    
    # キャッシュフロー情報から不要データを削る。
    cf_df = trim_unnecessary_from_dataframe(cf_df)
    
    # DataFrameを結合する    
    df = pd.concat([fin_df1, fin_df2, cf_df], axis=1)
    
    # ROAとROEを求める
    df['ROA'] = df['純利益'] / df['総資産'] * 100
    df['ROE'] = df['純利益'] / df['純資産'] * 100
    
    return df
    
##############################
# 指定した名称の<table>要素のデータを抽出する
##############################
def get_financial_table(bs, table_name):
    """ 指定した名称の<table>要素のデータを抽出する
    
    Args:
        bs          (BeautifulSoup) : 抽出対象HTMLのBeautifulSoupオブジェクト
        table_name  (string)        : 抽出対象テーブルの名称

    Returns:
        DataFrame  :  <table>要素を格納したDataFrame
    """
    
    # 全<table>要素を抽出
    table_all = bs.find_all('table')
    
    # 決算情報の<table>要素を検索する。
    fin_table1 = None
    for table in table_all:
        
        # <caption>要素を取得
        caption = table.find('caption')
        if caption is None:
            continue
        
        # <caption>要素の文字列が目的のものと一致したら終了
        if caption.text == table_name:
            fin_table1 = table
            break
    
    # <table>要素内のヘッダ情報を取得する。
    headers = []
    thead_th = fin_table1.find('thead').find_all('th')
    for th in thead_th:
        headers.append(th.text)
    
    # <table>要素内のデータを取得する。
    rows = []
    tbody_tr = fin_table1.find('tbody').find_all('tr')
    for tr in tbody_tr:
        
        # 1行内の全データを格納するためのリスト
        row = []
        
        # <tr>要素内の<th>要素を取得する。
        th = tr.find('th')
        row.append(th.text)
        
        # <tr>要素内の<td>要素を取得する。
        td_all = tr.find_all('td')
        for td in td_all:
            row.append(td.text)
        
        # 1行のデータを格納したリストを、リストに格納
        rows.append(row)
        
    # DataFrameを生成する
    df = pd.DataFrame(rows, columns=headers)
    df = df.set_index(headers[0])   # 先頭の列(決算期)をインデックスに指定する
    
    return df
        
##############################
# キャッシュフロー情報を抽出する
##############################
def get_cf_table(bs):
    """ キャッシュフロー情報を抽出する
    
    Args:
        bs  (BeautifulSoup) : 抽出対象HTMLのBeautifulSoupオブジェクト

    Returns:
        DataFrame  :  <table>要素を格納したDataFrame
    """
    
    # 全<table>要素を抽出
    table_all = bs.find_all('table')
    
    # キャッシュフロー情報の<table>要素を検索する。
    cf_table = None
    for table in table_all:
        
        # <thead>要素を取得
        thead = table.find('thead')
        if thead is None:
            continue
        
        # <thead>内の全<th>要素を取得
        thead_th = thead.find_all('th')
        for th in thead_th:
            if th.text == '営業CF':
                cf_table = table
                break
    
    # <table>要素内のヘッダ情報を取得する。
    headers = []
    thead_th = cf_table.find('thead').find_all('th')
    for th in thead_th:
        headers.append(th.text)
    
    # <table>要素内のデータを取得する。
    rows = []
    tbody_tr = cf_table.find('tbody').find('tr').find_all('tr')
    for tr in tbody_tr:
        
        # 1行内の全データを格納するためのリスト
        row = []
        
        # <tr>要素内の<th>要素を取得する。
        th = tr.find('th')
        row.append(th.text)
        
        # <tr>要素内の<td>要素を取得する。
        td_all = tr.find_all('td')
        for td in td_all:
            row.append(td.text)
        
        # 1行のデータを格納したリストを、リストに格納
        rows.append(row)

    # DataFrameを生成する
    df = pd.DataFrame(rows, columns=headers)
    df = df.set_index(headers[0])   # 先頭の列(決算期)をインデックスに指定する
    
    return df
    
##############################
# DataFrameから不要なデータを削る。
##############################
def trim_unnecessary_from_dataframe(df):
    """ DataFrameから不要なデータを削る。
    
    Args:
        df  (DataFrame) : データフレーム

    Returns:
        DataFrame   : 不要データ削除後のDataFrame
    """
    
    # 数値のカンマを削除する関数
    def trim_camma(x):
        # 2,946,639.3のようなカンマ区切り、小数点有りの数値か否か確認する
        comma_re = re.search(r"([+-]?\d{1,3}(,\d{3})*(\.\d+){0,1})", x)
        if comma_re:
            value = comma_re.group(1)
            value = value.replace(',', '') # カンマを削除
            return np.float64(value) # 数値に変換
        
        return x
    
    # 各列に対して、trim_cammaを適用する
    new_df = df.copy()
    for col in df.columns:
        new_df[col] = df[col].map(lambda v : trim_camma(v))
    
    # 括弧内の文字列を削除する関数(括弧自体も削除する)
    def remove_inparentheses(s):
        
        # インデックス(決算情報)の括弧内要素を削除する。
        #   ex) 決算期(決算発表)
        result = re.search(r"(.+)(\(.+\))", s)
        if result:
            str = result.group(1)
            return str
        
        return s
    
    # インデックス(決算情報)の括弧内要素を削除する。
    new_df.index.name = remove_inparentheses(new_df.index.name)
    new_df.index = new_df.index.map(lambda s : remove_inparentheses(s))
    
    return new_df
    
##############################
# 複数銘柄の決算情報を整形する
##############################
def reshape_financial_info(df):
    """ 複数銘柄の決算情報を整形する。
    
    Args:
        df  (DataFrame) : 複数銘柄の決算情報が格納されたデータフレーム

    Returns:
        DataFrame   : 整形後のDataFrame
    """
    
    # 各銘柄のデータと統計量を結合する。
    new_df = df.copy()
    
    # 売上高(百万円)    -> 売上高(十億円)
    # 営業利益(百万円)　-> 営業利益(十億円)
    # 経常利益(百万円)  -> 経常利益(十億円)
    # 純利益(百万円)    -> 純利益(十億円)
    # 総資産(百万円)    -> 総資産(十億円)
    # 純資産(百万円)    -> 純資産(十億円)
    # 営業CF(百万円)    -> 営業CF(十億円)
    # 投資CF(百万円)    -> 投資CF(十億円)
    # 財務CF(百万円)    -> 財務CF(十億円)
    # 現金期末残高(百万円)    -> 現金期末残高(十億円)
    # フリーCF(百万円)  -> フリーCF(十億円)
    new_df['売上高'] = new_df['売上高'] / 1.0e+3
    new_df['営業利益'] = new_df['営業利益'] / 1.0e+3
    new_df['経常利益'] = new_df['経常利益'] / 1.0e+3
    new_df['純利益'] = new_df['純利益'] / 1.0e+3
    new_df['総資産'] = new_df['総資産'] / 1.0e+3
    new_df['純資産'] = new_df['純資産'] / 1.0e+3
    new_df['営業CF'] = new_df['営業CF'] / 1.0e+3
    new_df['投資CF'] = new_df['投資CF'] / 1.0e+3
    new_df['財務CF'] = new_df['財務CF'] / 1.0e+3
    new_df['現金期末残高'] = new_df['現金期末残高'] / 1.0e+3
    new_df['フリーCF'] = new_df['フリーCF'] / 1.0e+3
    new_df = new_df.rename(columns={
        '売上高'        : '売上高(十億円)', 
        '営業利益'      : '営業利益(十億円)',
        '経常利益'      : '経常利益(十億円)',
        '純利益'        : '純利益(十億円)',
        '1株益'         : '1株益(円)',
        '1株純資産'     : '1株純資産(円)',
        '総資産'        : '総資産(十億円)',
        '純資産'        : '純資産(十億円)',
        '営業CF'        : '営業CF(十億円)',
        '投資CF'        : '投資CF(十億円)',
        '財務CF'        : '財務CF(十億円)',
        '現金期末残高'  : '現金期末残高(十億円)',
        'フリーCF'      : 'フリーCF(十億円)',
    })
    
    return new_df
    
##################################################
# 決算情報のうち指定したデータを棒グラフで可視化する
##################################################
def visualize_financial_info_in_bar(df, data_name, filepath):
    """ 決算情報のうち指定したデータを棒グラフで可視化する
    
    Args:
        df          (DataFrame) : 複数銘柄の基本情報が格納されたデータフレーム
        data_name   (string)    : 可視化する列名
        filepath    (string)    : 可視化したグラフを保存するファイルパス
    
    Returns:
    """
    
    # FigureとAxesを取得
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    
    # 銘柄の名称リスト
    brand_names = list(df.index.unique('名称'))
    
    # 全銘柄のデータを折れ線グラフに表示
    for brand_name in brand_names:
        
        brand_df = df.loc[(brand_name,)]    # 指定した銘柄のデータ
        x = brand_df.index                  # 決算期
        y = brand_df[data_name]             # 可視化するデータ
        
        # 折れ線グラフ表示
        ax.plot(x, y, marker='o')
    
    # 補助線を描画
    ax.grid(axis='y', color='gray', ls='--')
    
    # 軸ラベルをセット
    plt.xlabel(data_name, size=15)
    
    # 凡例を表示
    ax.legend(brand_names)
    
    # グラフを表示
    fig.show()
    fig.savefig(filepath)
    
##################################################
# 決算情報のうち指定した複数データを
# 折れ線グラフで可視化する
##################################################
def visualize_financial_infos_in_line(df, data_names, filepath, from_zero=False):
    """ 決算情報のうち指定した複数データを折れ線グラフで可視化する
    
    Args:
        df          (DataFrame) : 複数銘柄の基本情報が格納されたデータフレーム
        data_names  (list)      : 可視化する列名のリスト
        filepath    (string)    : 可視化したグラフを保存するファイルパス
    
    Returns:
    """
    
    data_num = len(data_names)
    
    # サブプロットの行数・列数を決定
    if data_num == 1:
        rows, cols = (1, 1)
        figsize=(6, 4)
    elif data_num == 2:
        rows, cols = (1, 2)
        figsize=(10, 4)
    elif data_num == 3:
        rows, cols = (1, 3)
        figsize=(15, 4)
    elif data_num == 4:
        rows, cols = (2, 2)
        figsize=(10, 8)
    elif data_num <= 6:
        rows, cols = (2, 3)
        figsize=(15, 8)
    elif data_num <= 9:
        rows, cols = (3, 3)
        figsize=(15, 12)
    else:
        rows, cols = (4, 4)
        figsize=(20, 16)
        
    # Figurを取得
    fig = plt.figure(figsize=figsize)
    #fig = plt.figure()
    
    # 指定した全データをデータ別に折れ線グラフで表示する
    for i in range(data_num):
        
        # Axesを取得
        ax = fig.add_subplot(rows, cols, i+1)
        
        # データ名
        data_name = data_names[i]
        
        # 銘柄の名称リスト
        brand_names = list(df.index.unique('名称'))
        
        # 全銘柄のデータを折れ線グラフに表示
        for brand_name in brand_names:
            
            brand_df = df.loc[(brand_name,)]    # 指定した銘柄のデータ
            x = brand_df.index                  # 決算期
            y = brand_df[data_name]             # 可視化するデータ
            
            # 折れ線グラフ表示
            ax.plot(x, y, marker='o')
        
        # 補助線を描画
        ax.grid(axis='y', color='gray', ls='--')
        
        # 軸ラベルをセット
        plt.xlabel(data_name, size=15)
        
        # 凡例を表示
        ax.legend(brand_names)
        
        # Y軸の表示範囲を設定
        if from_zero:
            ax.set_ylim(ymin=0)
    
    # 不要な余白を削る
    plt.tight_layout()
    
    # グラフを表示
    fig.show()
    fig.savefig(filepath)

##############################
# 決算情報のうちROEとROAを可視化する
##############################
def visualize_roe_roa(df, filepath):
    """ 決算情報のうち指定した複数データを可視化する
    
    Args:
        df          (DataFrame) : 複数銘柄の基本情報が格納されたデータフレーム
        filepath    (string)    : 可視化したグラフを保存するファイルパス
    
    Returns:
    """
    
    # 可視化するデータ
    data_names = ['ROE', 'ROA']

    # Figurを取得
    fig = plt.figure(figsize=(9.6, 4.8))

    # 指定した全データをデータ別に折れ線グラフで表示する
    for i, data_name in enumerate(data_names):
        
        # Axesを取得
        ax = fig.add_subplot(1, 2, i+1)
        
        # 銘柄の名称リスト
        brand_names = list(df.index.unique('名称'))
        
        # 全銘柄のデータを折れ線グラフに表示
        for brand_name in brand_names:
            
            brand_df = df.loc[(brand_name,)]    # 指定した銘柄のデータ
            x = brand_df.index                  # 決算期
            y = brand_df[data_name]             # 可視化するデータ
            
            # 折れ線グラフ表示
            ax.plot(x, y, marker='o')
        
        # 補助線を描画
        ax.grid(axis='y', color='gray', ls='--')
        
        # 軸ラベルをセット
        plt.xlabel(data_name, size=15)
        
        # 凡例を表示
        ax.legend(brand_names)
    
    # 不要な余白を削る
    plt.tight_layout()
    
    # グラフを表示
    fig.show()
    fig.savefig(filepath)

##################################################
# 決算情報のうち指定した１銘柄の指定データを可視化する
##################################################
def visualize_financial_info_for_specified_brand(df, brand_name, bar_datas, line_datas=None, filepath=None):
    """ 決算情報のうち指定した１銘柄の指定データを可視化する
    
    Args:
        df          (DataFrame) : 複数銘柄の基本情報が格納されたデータフレーム
        brand_name  (string)    : 可視化する銘柄の名称
        bar_datas   (list)      : 棒グラフで可視化する列名のリスト
        line_datas  (list)      : 折れ線グラフで可視化する列名のリスト
        filepath    (string)    : 可視化したグラフを保存するファイルパス
    
    Returns:
    """
    
    # 可視化するデータを抽出
    brand_df = df.loc[(brand_name,)]        # 指定した銘柄
    fiscal_year = brand_df.index.values     # 決算期
    
    # データ数を取得
    num_year = len(fiscal_year)     # 可視化する決算期の数
    num_bar_data = len(bar_datas)   # 棒グラフで可視化するデータ数
    
    # FigureとAxesを取得
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    
    # 色
    color_count = 0
    colors = plt.get_cmap('tab10')
    
    ########################################
    # 棒グラフの可視化処理
    ########################################
    
    # 棒グラフを横並びで表示するためのパラメータ
    width = 0.8 / num_bar_data      # 棒グラフの幅
    xpos = np.arange(num_year)      # X軸上の位置
    
    # 可視化するデータ数分ループ
    for i, data_name in enumerate(bar_datas):
        
        x = xpos + width * i
        y = brand_df[data_name]
        
        # 棒グラフを表示
        ax1.bar(x, y, width=width, align='center', label=data_name, color=colors(color_count))
        color_count += 1
        
    # X軸の目盛位置を調整し、銘柄名を表示
    offset = width / 2 * (num_bar_data - 1)
    ax1.set(xticks=xpos+offset, xticklabels=fiscal_year)
    
    # Y軸の表示範囲を設定
    ymin, ymax = get_yminmax_financial_info(brand_df, bar_datas)
    ax1.set_ylim(ymin=ymin*1.5, ymax=ymax*1.5)
    
    ########################################
    # 折れ線グラフの可視化処理
    ########################################
    if line_datas is not None:
        
        # 右軸のAxesを取得
        ax2 = ax1.twinx()
        
        # 可視化するデータ数分ループ
        for i, data_name in enumerate(line_datas):
            
            # 折れ線グラフ表示
            y = brand_df[data_name]
            ax2.plot(xpos+offset, y, marker='o', label=data_name, color=colors(color_count))
            color_count += 1
            
        # Y軸の表示範囲を設定
        ymin, ymax = get_yminmax_financial_info(brand_df, line_datas)
        ax2.set_ylim(ymin=ymin*1.3, ymax=ymax*1.3)

    # 補助線を描画
    ax1.grid(axis='y', color='gray', ls='--')
    
    # 凡例を表示
    h1, l1 = ax1.get_legend_handles_labels()
    if line_datas is None:
        ax1.legend(h1, l1, loc='upper right')
    else:
        h2, l2 = ax2.get_legend_handles_labels()
        ax1.legend(h1+h2, l1+l2, loc='upper right')
    
    # グラフのタイトルを追加
    plt.title(brand_name)

    # グラフを表示
    fig.show()
    
    # グラフをファイルに出力
    if filepath is not None:
        fig.savefig(filepath)    
    
    
##################################################
# 指定した列を可視化する際のY軸の表示範囲を取得する
##################################################
def get_yminmax_financial_info(df, columns):
    """ 指定した列を可視化する際のY軸の表示範囲を取得する
    
    Args:
        df          (DataFrame) : 複数銘柄の決算情報が格納されたデータフレーム
        columns     (list)      : 可視化する列
    
    Returns:
        tuple   : Y軸の表示範囲を(ymin, ymax)の形で返す
    """
        
    # 最大値・最小値を取得
    ymax = df[columns].max().max() 
    ymin = df[columns].min().min()
    
    if ymin >= 0:
        return(0, ymax)
    else:
        abs_max = max([abs(ymin), ymax])
        return(-abs_max, abs_max)
    