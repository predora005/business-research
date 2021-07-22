# coding: utf-8

from pltinit import *
from stock import *
import datetime
import os

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    #  matplotlibの日本語フォント設定処理
    plt_font_init()
    
    # 銘柄コード
    # codes = ['9020.JP', '9984.JP', '2193.JP', '3402.JP']
    # 9020.JP:JR東日本、9984.JP:ソフトバンク、2193.JP:クックパッド、3402.JP：東レ
    # codes = ['VOO', 'VT', 'VTI']
    codes = ['GOOGL', 'AAPL', 'FB', 'AMZN', 'MSFT']
    dirpath = os.getcwd()
    
    # 取得開始日と終了日
    start_date = datetime.datetime(2021, 4, 1)
    end_date = None
    
    # 各銘柄の株価取得・チャート作成を実行する
    for code in codes:
    
        # 指定銘柄コードの株価を取得・更新する
        df = update_stock_prices(dirpath, code, start_date, end_date)
        #print('==========')
        #print('[update_stock_prices]')
        #print(df)
        
        # テクニカル指標を追加する
        df = add_technical_indicators(df)
        #print('==========')
        #print('[add_technical_indicators]')
        #print(df)
        
        # ロウソク足チャートを保存
        save_stock_chart(df, dirpath, code)
        
    
    # テクニカル指標分析によるアラートを出力する
    make_tech_alerts(dirpath, codes)
        
    