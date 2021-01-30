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
    tables = json['GET_STATS_LIST']['DATALIST_INF']['TABLE_INF']
    #print('==================================================')
    #print(datalist)
    
    # ディクショナリ形式にし、pandasのDataFrameに変換
    dict_list = []
    for table in tables:
        #print('==================================================')
        #print(data)
        dict = {}
        
        # 統計表ID
        dict['id'] = table['@id']
        
        # 政府統計コードと統計名
        dict['stat_id'] = table['STAT_NAME']['@code']
        dict['stat_name'] = table['STAT_NAME']['$']
        
        #タイトル
        if '$' in table['TITLE']:
            dict['title'] = table['TITLE']['$']
        else:
            dict['title'] = table['TITLE']
        
        # 担当機関
        dict['gov_code'] = table['GOV_ORG']['@code']
        dict['gov_name'] = table['GOV_ORG']['$']
        
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
def get_meta_info(app_id, stats_data_id):

    # メタ情報取得のURL
    url = 'https://api.e-stat.go.jp/rest/3.0/app/json/getMetaInfo?'
    url += 'appId={0:s}&'.format(app_id) 
    url += 'statsDataId={0:s}&'.format(stats_data_id)
    url += 'explanationGetFlg=N&'   # 解説情報有無
    #url += 'limit=3'
    print(url)
    
    # メタ情報取得
    json = requests.get(url).json()
    #print('==================================================')
    #print(json)
    
    # メタ情報から各表のデータ部取得
    classes = json['GET_META_INFO']['METADATA_INF']['CLASS_INF']['CLASS_OBJ']
    #print('==================================================')
    #print(classes)
    
    # Key:分類名、Value：項目名のリストのディクショナリを作成
    class_dict = {}
    for class_obj in classes:
        class_name = class_obj['@name']
        
        # 分類内の項目をリストに追加
        class_list = []
        for item in class_obj['CLASS']:
            item_name = item['@name']
            class_list.append(item_name)
        
        # ディクショナリに追加
        class_dict[class_name] = class_list
    
    print('==================================================')
    print(class_dict)
    
    return class_dict
    
##################################################
# 統計データ取得
##################################################
def get_stats_data_info(app_id, stats_data_id):

    # 統計データ取得のURL
    url = 'https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData?'
    url += 'appId={0:s}&'.format(app_id) 
    url += 'statsDataId={0:s}&'.format(stats_data_id)
    url += 'metaGetFlg=N&'          # メタ情報有無
    url += 'explanationGetFlg=N&'   # 解説情報有無
    url += 'annotationGetFlg=N&'    # 注釈情報有無
    #url += 'limit=3'
    print(url)
    
    # 統計データ取得
    json = requests.get(url).json()
    print('==================================================')
    #print(json)
    
    # 統計データからデータ部取得
    data = json['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']
    print('==================================================')
    #print(data)
    
    # jsonからDataFrameを作成
    values = data['VALUE']
    df = pd.DataFrame(values)
    print('==================================================')
    print(df)
    
    return df
    
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
    #get_stats_list(app_id)
    
    # メタ情報取得
    meta_info = get_meta_info(app_id, '0003411561')
    
    # 統計データ取得
    stats_data = get_stats_data_info(app_id, '0003411561')
    
    
