# coding: utf-8

import requests
from bs4 import BeautifulSoup
import time
import numpy as np
import pandas as pd
import re

##############################
# 指定した複数銘柄の基本情報を取得する
##############################
def get_basic_infos(codes):
    """ 指定した複数銘柄の基本情報を取得する。
    
    Args:
        codes   (dict)  : 証券コードと名称のディクショナリ
                          (ex){'JR東日本':9020, 'JR西日本': 9021}
    Returns:
        string  : 取得した情報を格納したディクショナリ
    """
    
    basic_df = None
    for name in codes.keys():
        
        code = codes[name]
        basic_info = get_basic_info(code)
        
        # ディクショナリからSeriesを生成
        sr = pd.Series(basic_info.values(), index=basic_info.keys(), name=name)

        if basic_df is None:
            basic_df = pd.DataFrame([sr])
        else:
            basic_df = basic_df.append(sr)
        
        # 1秒ディレイ
        time.sleep(1)

    return basic_df

##############################
# 指定した銘柄の基本情報を取得する
##############################
def get_basic_info(code):
    """ 指定した銘柄の基本情報を取得する。
    
    Args:
        code    (int) : 証券コード

    Returns:
        dict: 取得した情報
    """
    # 指定URLのHTMLデータを取得
    url = "https://minkabu.jp/stock/{0:d}".format(code)
    html = requests.get(url)
    
    # BeautifulSoupのHTMLパーサーを生成
    soup = BeautifulSoup(html.content, "html.parser")
    
    # データ格納用のディクショナリを準備
    basic_info = {}
    
    # 全<li>要素を抽出
    li_all = soup.find_all('li')
    
    for li in li_all:
        
        # <li>要素内の<dt>要素を抽出
        dt = li.find('dt')
        if dt is None:
            # <dt>要素がなければ処理不要
            continue
        
        # <li>要素内の<dd>要素を抽出
        dd = li.find('dd')
        
        # <dt><dd>要素から文字列を取得
        key = dt.text
        value = dd.text
        
        # ディクショナリに格納
        basic_info[key] = value
        
    return basic_info
    
##############################
# DataFrameから単位を削る。
##############################
def trim_unit_from_dataframe(df):
    """ DataFrameから単位を削る。
    
    Args:
        df  (DataFrame) : データフレーム

    Returns:
        new_df  : 単位削除後のDataFrame
    """
    
    # 単位を削除する関数
    def trim_unit(x):
        
        # 単位=円を削除
        yen_re = re.search(r"(\d{1,3}(,\d{3})*\.\d+)円", x)
        if yen_re:
            value = yen_re.group(1)
            value = value.replace(',', '')
            return np.float64(value)
        
        # 単位=%を削除
        per_re = re.search(r"(\d+\.\d+)%", x)
        if per_re:
            value = per_re.group(1)
            return np.float64(value)
        
        # 単位=株を削除
        st_re = re.search(r"(\d{1,3}(,\d{3})*)株", x)
        if st_re:
            value = st_re.group(1)
            value = value.replace(',', '')
            return np.int64(value)
        
        # 単位=倍を削除
        times_re = re.search(r"(\d+\.\d+)倍", x)
        if times_re:
            value = times_re.group(1)
            return np.float64(value)
        
        # 単位=百万円を削除
        million_yen_re = re.search(r"(\d{1,3}(,\d{3})*)百万円", x)
        if million_yen_re:
            value = million_yen_re.group(1)
            value = value.replace(',', '')
            value = np.int64(value) * 1000000
            return value
        
        # 単位=千株を削除
        thousand_st_re = re.search(r"(\d{1,3}(,\d{3})*)千株", x)
        if thousand_st_re:
            value = thousand_st_re.group(1)
            value = value.replace(',', '')
            value = np.int64(value) * 1000
            return value
        
        return x
    
    # 各列に対して、trim_unitを適用する
    new_df = df.copy()
    for col in df.columns:
        new_df[col] = df[col].map(lambda v : trim_unit(v))

    return new_df

##############################
# 複数銘柄の基本情報を整形する
##############################
def reshape_basic_info(df):
    """ 複数銘柄の基本情報を整形する。
    
    Args:
        df  (DataFrame) : 複数銘柄の基本情報が格納されたデータフレーム

    Returns:
        new_df  : 整形後のDataFrame
    """
    
    # DataFrameから単位を削る。
    new_df = trim_unit_from_dataframe(df)

    # 統計量(平均値と標準偏差)を算出する。
    statistics = pd.DataFrame({'平均値': new_df.mean(), '標準偏差': new_df.std()})

    # 各銘柄のデータと統計量を結合する。
    new_df = new_df.append(statistics.T)
    
    # 出来高,時価総額,発行済株数の単位を変換する。
    new_df['出来高'] = new_df['出来高'] / 1.0e+3
    new_df['時価総額'] = new_df['時価総額'] / 1.0e+12
    new_df['発行済株数'] = new_df['発行済株数'] / 1.0e+6
    new_df = new_df.rename(columns={
        '出来高'        : '出来高(千株)', 
        '時価総額'      : '時価総額(兆円)',
        '発行済株数'    : '発行済株数(百万株)', 
    })
    
    # 不要な列を削除する。
    new_df = new_df.drop(columns=['始値', '高値', '安値', '単元株数', '購入金額'])
    
    return new_df
    