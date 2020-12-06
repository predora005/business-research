# coding: utf-8

from stinfo import *
import datetime

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    # matplotlibの日本語フォント設定
    plt_font_init()
    
    code = 9020
    start_year = 2016
    end_year = 2020
    
    # 指定した銘柄の株価を取得する
    df = get_stock_price(code, start_year, end_year)
    #print(df.head())
    #print(df.dtypes)
    
    # 株価情報のデータタイプを修正する
    df = astype_stock_price(df)
    #print(df.dtypes)

    # 株価情報に移動平均を追加する
    df = add_moving_average_stock_price(df)
    
    # 2020/01/01以降のデータを抽出
    df = df['2020-01-01':]
    print(df.head())
    
    # 株価を折れ線グラフで可視化する
    visualize_stock_price_in_line(df, title='JR東日本', show_average=True, filepath='jr_east_price.png')
    
    