# coding: utf-8

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

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
        print(sr)
        
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
    

    