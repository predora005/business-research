# coding: utf-8

from stinfo import *
import pandas as pd
import re

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
    df = get_basic_infos(codes)
    print(df)
    
    # 複数銘柄の基本情報を整形する
    df2 = reshape_basic_info(df)
    print(df2)
    
    # 複数銘柄の基本情報を可視化する
    df = df2.drop(index='標準偏差')
    visualize_basic_info(df, ['PER(調整後)'], 'per.png')
    visualize_basic_info(df, ['PSR', 'PBR'], 'psr_pbr.png')
    visualize_basic_info(df, ['時価総額(兆円)'], 'market_cap.png')

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
    
    ## '標準偏差'の列を削除
    #df = df2.drop(index='標準偏差')
    #
    ## FigureとAxesを取得
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    #
    #per = df['PER(調整後)']     # PER
    #xpos = np.arange(len(per))  # X軸上の位置
    #
    ## 棒グラフを作成
    #ax.bar(xpos, per)
    #
    ## X軸に銘柄名を表示
    #ax.set(xticks=xpos, xticklabels=df.index)
    #
    ## 補助線を描画する
    #ax.grid(axis='y', color='gray', ls='--')
    #
    ## 凡例を表示
    #ax.legend(['PER(調整後)'])
    #
    ## グラフを表示
    #fig.show()
    #fig.savefig('test.png')


