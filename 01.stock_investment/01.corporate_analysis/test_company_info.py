# coding: utf-8

from stinfo import *
import pandas as pd
import re

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
    df = get_basic_infos(codes)
    print(df)
    
    df2 = reshape_basic_info(df)
    print(df2)
    

    #jre_dict = get_basic_info(9020)
    #jrw_dict = get_basic_info(9022)
    #jrc_dict = get_basic_info(9021)
    #tokyu_dict = get_basic_info(9005)
    #kintetsu_dict = get_basic_info(9041)
    #
    #jre_sr = pd.Series(jre_dict.values(), index=jre_dict.keys(), name='JR東日本')
    #jrw_sr = pd.Series(jrw_dict.values(), index=jrw_dict.keys(), name='JR西日本')
    #jrc_sr = pd.Series(jrc_dict.values(), index=jrc_dict.keys(), name='JR東海')
    #tokyu_sr = pd.Series(tokyu_dict.values(), index=tokyu_dict.keys(), name='東急')
    #kintetsu_sr = pd.Series(kintetsu_dict.values(), index=kintetsu_dict.keys(), name='近鉄')
    #
    #df = pd.DataFrame([jre_sr, jrw_sr, jrc_sr, tokyu_sr, kintetsu_sr])
    
