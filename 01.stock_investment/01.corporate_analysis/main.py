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
    
    # DataFrameから単位を削る。
    df2 = trim_unit_from_dataframe(df)
    print(df2)
    print(df2.dtypes)
    
    # 統計量(平均値と標準偏差)を算出する。
    statistics = pd.DataFrame({'平均値': df2.mean(), '標準偏差': df2.std()})
    print(statistics)
    
    # 各銘柄のデータと統計量を結合する。
    df3 = df2.append(statistics.T)
    
    # 出来高と時価総額の単位を変換する。
    df3['出来高'] = df3['出来高'] / 1.0e+3
    df3['時価総額'] = df3['時価総額'] / 1.0e+12
    df3 = df3.rename(columns={'出来高': '出来高(千株)', '時価総額': '時価総額(兆円)'})
    
    # 不要な列を削除する。
    df3 = df3.drop(columns=['始値', '高値', '安値', '単元株数', '発行済株数', '購入金額'])
    print(df3)
    
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
    
