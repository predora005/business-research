# coding: utf-8

from stinfo import *

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    # matplotlibの日本語フォント設定
    plt_font_init()
    
    codes = {
        'JR東日本'  : 9020, 
        'JR西日本'  : 9022, 
        'JR東海'    : 9021, 
        '東急'      : 9005, 
        '近鉄'      : 9041,
    }
    
    # 指定した複数銘柄の基本情報を取得する。
    df = get_financial_infos(codes)

    # ROAとROEを求める
    df['ROA'] = df['純利益'] / df['総資産'] * 100
    df['ROE'] = df['純利益'] / df['純資産'] * 100
    print(df)
    
    # ROEとROAを可視化する
    visualize_financial_info(df, 'ROE', 'roe.png')
    visualize_financial_info(df, 'ROA', 'roa.png')
    
    visualize_financial_infos(df, ['売上高'], 'test1.png')
    visualize_financial_infos(df, ['ROA', 'ROE'], 'test2.png')
    visualize_financial_infos(df, ['売上高', '営業利益', '経常利益'], 'test3.png')
    visualize_financial_infos(df, ['売上高', '営業利益', '経常利益', '純利益'], 'test4.png')
    
    #code = 9020
    #
    ## 指定した証券コードの決算情報を取得する。
    #df = get_financial_info(code)
    #print(df)
    #
    ## 決算情報から不要データを削る。
    #df2 = trim_unnecessary_from_dataframe(df)
    #print(df2)
    
    