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
        'JR東海'    : 9022, 
        'JR西日本'  : 9021, 
        '東急'      : 9005, 
        '近鉄'      : 9041,
    }
    
    # 指定した複数銘柄の基本情報を取得する。
    df = get_financial_infos(codes)

    # ROAとROEを求める
    df['ROA'] = df['純利益'] / df['総資産'] * 100
    df['ROE'] = df['純利益'] / df['純資産'] * 100

    # 複数銘柄の決算情報を整形する
    df = reshape_financial_info(df)
    
    print(df)
        
    # ROEとROAを可視化する
    visualize_financial_info_in_bar(df, 'ROE', 'roe.png')
    visualize_financial_info_in_bar(df, 'ROA', 'roa.png')
    
    # ROEとROAをセットで可視化する
    visualize_roe_roa(df, 'roe_roa.png')
    
    # 決算情報のうち指定した複数データを可視化する
    visualize_financial_infos_in_line(df, ['自己資本率'], 'test1.png', from_zero=True)
    visualize_financial_infos_in_line(df, ['ROA', 'ROE'], 'test2.png', from_zero=True)
    visualize_financial_infos_in_line(df, ['純利益(十億円)', '総資産(十億円)', '純資産(十億円)'], 'test3.png', from_zero=True)
    visualize_financial_infos_in_line(df, ['売上高(十億円)', '営業利益(十億円)', '経常利益(十億円)', '純利益(十億円)'], 'test4.png', from_zero=True)
    visualize_financial_infos_in_line(df, ['営業CF(十億円)', '投資CF(十億円)', '財務CF(十億円)', '現金期末残高(十億円)'], 'test5.png', from_zero=False)
    
    # 決算情報のうち指定した１銘柄の指定データを可視化する
    ##############################
    # JR東日本
    visualize_financial_info_for_specified_brand(
        df, 'JR東日本', bar_datas=['営業利益(十億円)', '経常利益(十億円)', '純利益(十億円)'], 
        line_datas=['売上高(十億円)'], filepath='jr_east_pl.png')
    visualize_financial_info_for_specified_brand(
        df, 'JR東日本', bar_datas=['総資産(十億円)', '純資産(十億円)'], 
        line_datas=['ROA'], filepath='jr_east_bs.png')
    visualize_financial_info_for_specified_brand(
        df, 'JR東日本', bar_datas=['営業CF(十億円)', '投資CF(十億円)', '財務CF(十億円)'], 
        line_datas=['現金期末残高(十億円)'], filepath='jr_east_cf.png')
    ##############################
    # JR東海
    visualize_financial_info_for_specified_brand(
        df, 'JR東海', bar_datas=['営業利益(十億円)', '経常利益(十億円)', '純利益(十億円)'], 
        line_datas=['売上高(十億円)'], filepath='jr_central_pl.png')
    visualize_financial_info_for_specified_brand(
        df, 'JR東海', bar_datas=['総資産(十億円)', '純資産(十億円)'], 
        line_datas=['ROA'], filepath='jr_central_bs.png')
    visualize_financial_info_for_specified_brand(
        df, 'JR東海', bar_datas=['営業CF(十億円)', '投資CF(十億円)', '財務CF(十億円)'], 
        line_datas=['現金期末残高(十億円)'], filepath='jr_central_cf.png')

    #code = 9020
    #
    ## 指定した証券コードの決算情報を取得する。
    #df = get_financial_info(code)
    #print(df)
    #
    ## 決算情報から不要データを削る。
    #df2 = trim_unnecessary_from_dataframe(df)
    #print(df2)
    
    