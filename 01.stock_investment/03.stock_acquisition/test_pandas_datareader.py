# coding: utf-8

import pandas_datareader.data as web
#import datetime

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    # ダウ平均をSqooqで取得
    f = web.DataReader('^DJI', 'stooq')
    print(f.head())
    