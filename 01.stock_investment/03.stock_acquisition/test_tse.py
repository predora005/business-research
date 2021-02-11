# coding: utf-8

from tse import *
import datetime
import pandas as pd
#from tse import tse

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    #  matplotlibの日本語フォント設定処理
    plt_font_init()
    
    # 東証上場銘柄一覧を取得
    tse_brand_list = get_tse_brand_list('data_j.csv')
    
    # TOPIX500の銘柄を抽出し、33業種コード,33業種区分ごとの銘柄数を算出
    tse1 = tse_brand_list[tse_brand_list['市場・商品区分'] == '市場第一部（内国株）']
    #topix500 = tse1[(tse1['規模区分'] == 'TOPIX Core30')]
    topix500 = tse1[(tse1['規模区分'] == 'TOPIX Core30') | 
                    (tse1['規模区分'] == 'TOPIX Large70') |
                    (tse1['規模区分'] == 'TOPIX Mid400')]
    category_count = topix500.groupby(['33業種コード','33業種区分']).size()
    print(category_count)
    
    # TOPIX500銘柄の業界ごと株価上昇率を取得する
    #category_df, brand_df = get_tse_increase_rate_by_industry(
    #        topix500, datetime.datetime(2020, 11, 2))
    
    # 株価上昇率をCSVファイルに出力する
    #category_df.to_csv('topix500_category_increase_rate.csv')
    #brand_df.to_csv('topix500_brand_increase_rate.csv')
    
    category_df = pd.read_csv('topix500_category_increase_rate.csv', 
                            header=[0,1], index_col=0, parse_dates=True)
    brand_df = pd.read_csv('topix500_brand_increase_rate.csv',  
                            header=0, index_col=0)
    print(brand_df)
    
    # 業界ごと株価上昇率を折れ線グラフで可視化する
    visualize_tse_increase_rate_by_industry_in_line(
            category_df, 'topix500_category_increase_rate_in_line.png')
    
    # 業界ごと株価上昇率を棒グラフで可視化する
    visualize_tse_increase_rate_by_industry_in_bar(
            category_df, 'topix500_category_increase_rate_in_bar.png')
    
    # 東証銘柄の銘柄ごと株価上昇率の上位と下位を取得する
    df_top10 = get_tse_top_increase_rate_by_brands(brand_df, 10)
    print(df_top10)
    df_top10.to_csv('topix500_brand_increase_rate_top10.csv')
    
    df_bottom10 = get_tse_top_increase_rate_by_brands(brand_df, 10, bottom=True)
    print(df_bottom10)
    df_bottom10.to_csv('topix500_brand_increase_rate_bottom10.csv')
    
    # 
