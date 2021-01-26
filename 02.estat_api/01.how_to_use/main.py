# coding: utf-8

import sys
import requests
import pandas as pd

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    # コマンドライン引数からアプリケーションID取得
    if len(sys.argv) < 2:
        print('Usage:')
        print('  python3 {0:s} [appId]'.format(sys.argv[0]))
        sys.exit(1)
        
    app_id = sys.argv[1]
    
    # 統計表情報取得のURL
    url = 'https://api.e-stat.go.jp/rest/3.0/app/json/getStatsList?'
    url += 'appId={0:s}&'.format(app_id) 
    url += 'statsNameList=Y&'
    url += 'limit=5'
    print(url)
    
    # 統計表情報取得
    json = requests.get(url).json()
    print('==================================================')
    print(json)
    
    # 統計表情報から各表のデータ部取得
    datalist = json['GET_STATS_LIST']['DATALIST_INF']['LIST_INF']
    print('==================================================')
    print(datalist)
    
    # pandasのDataFrameに変換
    df = pd.DataFrame(datalist)
    print('==================================================')
    print(df.head())
    
    
