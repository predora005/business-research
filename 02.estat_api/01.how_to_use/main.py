# coding: utf-8

import sys
import requests
import pandas as pd

##################################################
# 統計表情報取得
##################################################
def get_stats_list(app_id):

    # 統計表情報取得のURL
    url = 'https://api.e-stat.go.jp/rest/3.0/app/json/getStatsList?'
    url += 'appId={0:s}&'.format(app_id) 
    #url += 'statsNameList=Y&'
    url += 'limit=100'
    print(url)
    
    # 統計表情報取得
    json = requests.get(url).json()
    #print('==================================================')
    #print(json)
    
    # 統計表情報から各表のデータ部取得
    datalist = json['GET_STATS_LIST']['DATALIST_INF']['TABLE_INF']
    #print('==================================================')
    #print(datalist)
    
    # ディクショナリ形式にし、pandasのDataFrameに変換
    dict_list = []
    for data in datalist:
        #print('==================================================')
        #print(data)
        dict = {}
        
        # 統計表ID
        dict['id'] = data['@id']
        
        # 政府統計コードと統計名
        dict['stat_id'] = data['STAT_NAME']['@code']
        dict['stat_name'] = data['STAT_NAME']['$']
        
        #タイトル
        if '$' in data['TITLE']:
            dict['title'] = data['TITLE']['$']
        else:
            dict['title'] = data['TITLE']
        
        # 担当機関
        dict['gov_code'] = data['GOV_ORG']['@code']
        dict['gov_name'] = data['GOV_ORG']['$']
        
        # ディクショナリをリストに追加
        dict_list.append(dict)
        #print(dict)
    
    print('==================================================')
    df = pd.DataFrame(dict_list)
    print(df)
    
    # CSVファイルに出力
    df.to_csv('list.csv')
    
##################################################
# メタ情報取得
##################################################
def get_meta_info(app_id, stat_id):

    # メタ情報取得のURL
    url = 'https://api.e-stat.go.jp/rest/3.0/app/json/getMetaInfo?'
    url += 'appId={0:s}&'.format(app_id) 
    url += 'statsDataId={0:s}&'.format(stat_id)
    url += 'explanationGetFlg=N&'
    #url += 'limit=3'
    print(url)
    
    # 統計表情報取得
    json = requests.get(url).json()
    print('==================================================')
    print(json)
    
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
    
    # 統計表情報取得
    get_stats_list(app_id)
    
    # メタ情報取得
    #get_meta_info(app_id, '0003288322')
    
    
