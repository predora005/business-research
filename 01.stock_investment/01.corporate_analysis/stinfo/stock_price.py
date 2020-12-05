# coding: utf-8

import requests
from bs4 import BeautifulSoup
import time

import pandas as pd

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
        #print(html)
        #print(html.content)
        
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
    