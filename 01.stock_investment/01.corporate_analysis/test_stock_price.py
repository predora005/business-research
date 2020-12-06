# coding: utf-8

from stinfo import *
import datetime

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    # matplotlibの日本語フォント設定
    plt_font_init()
    
    codes = {
        'JR東日本'  : 9020, 
#        'JR東海'    : 9022, 
        'JR西日本'  : 9021, 
#        '東急'      : 9005, 
#        '近鉄'      : 9041,
    }
    start_year = 2019
    end_year = 2020
    
    # 指定した複数銘柄の株価を取得する
    df = get_stock_prices(codes, start_year, end_year)

    # 2020/01/01以降のデータを抽出
    df = df.loc[pd.IndexSlice[:, '2020-01-01':], :]

    # 複数銘柄の株価を折れ線グラフで可視化する
    brand_names = list(df.index.unique('銘柄'))
    visualize_multi_stock_prices_in_line(df, brand_names, show_average=True, filepath='stock_chart.png')
    
    #code = 9020
    #start_year = 2016
    #end_year = 2020
    #
    ## 指定した銘柄の株価を取得する
    #df = get_stock_price(code, start_year, end_year)
    ##print(df.head())
    ##print(df.dtypes)
    #
    ## 株価情報のデータタイプを修正する
    #df = astype_stock_price(df)
    ##print(df.dtypes)
    #
    ## 2020/01/01以降のデータを抽出
    #df = df['2020-01-01':]
    #print(df.head())
    #
    ## 株価を折れ線グラフで可視化する
    #visualize_stock_price_in_line(df, title='JR東日本', show_average=True, filepath='jr_east_price.png')
    
    