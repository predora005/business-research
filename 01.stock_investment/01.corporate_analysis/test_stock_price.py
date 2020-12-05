# coding: utf-8

from stinfo import *

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    # matplotlibの日本語フォント設定
    plt_font_init()
    
    code = 9020
    start_year = 2019
    end_year = 2020
    
    df = get_stock_price(code, start_year, end_year)
    
    print(df.head())
    print(df.tail())
    print(df.dtypes)
    