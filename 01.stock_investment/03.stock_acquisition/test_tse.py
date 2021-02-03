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
    
    # 東証一部銘柄の業界ごと株価上昇率を取得する
    df = get_tse1_increase_rate_by_industry(tse_brand_list, datetime.datetime(2021, 1, 4))
    #print(df)
    