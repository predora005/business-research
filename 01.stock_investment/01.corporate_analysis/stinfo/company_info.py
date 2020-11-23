# coding: utf-8

import requests
from bs4 import BeautifulSoup

##############################
# 指定した銘柄の基本情報を取得する
##############################
def get_basic_info(code):
    """ URLを取得する。
    
    Args:
        code    (int) : 証券コード
        code    (int) : 証券コード

    Returns:
        string: URL
    """
    # 指定URLのHTMLデータを取得
    url = "https://minkabu.jp/stock/9020"
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