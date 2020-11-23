# coding: utf-8

from stinfo import *

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    codes = {
        'JR東日本'  : 9020, 
        'JR西日本'  : 9022, 
        'JR東海'    : 9021, 
        '東急'      : 9005, 
        '近鉄'      : 9041,
    }
    
    # 指定した複数銘柄の基本情報を取得する。
    df = get_financial_infos(codes)
    print(df)
    
    #code = 9020
    #
    ## 指定した証券コードの決算情報を取得する。
    #df = get_financial_info(code)
    #print(df)
    #
    ## 決算情報から不要データを削る。
    #df2 = trim_unnecessary_from_dataframe(df)
    #print(df2)
    
    