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
    code = '9020.JP'
    #code = '9984.JP'
    dirpath = os.getcwd()
    start_date = datetime.datetime(2021, 6, 1)
    end_date = None
    
    # 指定銘柄コードの株価を取得・更新する
    df = update_stock_prices(dirpath, code, start_date, end_date)
    print('==========')
    print('[update_stock_prices]')
    print(df)
    
    # テクニカル指標を追加する
    df = add_technical_indicators(df)
    print('==========')
    print('[add_technical_indicators]')
    print(df)
    
    # テクニカル指標分析によるアラートを出力する
    make_tech_alerts(df, dirpath, code)
    
    # ロウソク足チャートを保存
    #save_stock_chart(df, dirpath, code)
    
    