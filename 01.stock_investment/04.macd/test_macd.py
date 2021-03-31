# coding: utf-8

from pltinit import *
from stock import *
import datetime

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    #  matplotlibの日本語フォント設定処理
    plt_font_init()
    
    # 指定した銘柄コードの株価を取得する
    code = '9020.JP'
    start_date = datetime.datetime(2021, 3, 29)
    end_date   = datetime.datetime(2021, 3, 31)
    df = get_stock_prices(code, start_date, end_date)
    print(df)
    
