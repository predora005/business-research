# coding: utf-8

from stinfo import *

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    code = 9020
    
    # 指定した証券コードの決算情報を取得する。
    df = get_financial_info(code)
    print(df)

    # 決算情報から不要データを削る。
    df2 = trim_unnecessary_from_dataframe(df)
    print(df2)
    
    