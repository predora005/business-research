# coding: utf-8

import pandas_datareader as pdr
import pandas_datareader.data as web
import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    # 米国国債10年を5年分取得
    gs10 = pdr.get_data_fred('GS10')
    #print(gs10)
    
    # ダウ平均をSqooqで取得
    f = web.DataReader('^DJI', 'stooq')
    #print(f.head())
    
    # バンガード S&P500 ETF (VOO)の
    # 2020年以降の株価を取得
    voo = web.DataReader(
        'VOO', 'stooq', 
        start=datetime.datetime(2020, 1, 1)
    )
    #print(voo)
    
    # 年の昇順にソート
    #voo = voo.sort_values('Date')
    
    # 日本語フォントの設定
    mpl.font_manager._rebuild()    # キャッシュの削除
    plt.rcParams['font.family'] = 'IPAGothic'    # 日本語フォントを指定
    
    # 図と座標軸を取得
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    
    # 折れ線グラフをセット
    ax.plot(voo.index, voo['Close'], label='VOO')
    ax.grid(axis='y', color='gray', ls=':')
    ax.legend()
    
    # 折れ線グラフを表示
    fig.show()
    fig.savefig('voo.png')
