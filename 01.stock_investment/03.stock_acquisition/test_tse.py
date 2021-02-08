# coding: utf-8

from tse import *
import datetime
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
    topix500 = tse1[(tse1['規模区分'] == 'TOPIX Core30') | 
                    (tse1['規模区分'] == 'TOPIX Large70') |
                    (tse1['規模区分'] == 'TOPIX Mid400')]
    category_count = topix500.groupby(['33業種コード','33業種区分']).size()
    print(category_count)
    
    # TOPIX500銘柄の業界ごと株価上昇率を取得する
    category_df, brand_df = get_tse_increase_rate_by_industry(topix500, datetime.datetime(2020, 12, 1))
    #print(df)
    
    category_df.to_csv('topix500_category_increase_rate.csv')
    brand_df.to_csv('topix500_brand_increase_rate.csv')
