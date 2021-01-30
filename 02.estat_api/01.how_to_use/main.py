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
    
    df = pd.DataFrame(dict_list)
    print('==================================================')
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
    class_objs = json['GET_META_INFO']['METADATA_INF']['CLASS_INF']['CLASS_OBJ']
    print('==================================================')
    #print(class_objs)
    
    return class_objs
    
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
    #print('==================================================')
    #print(json)
    
    # 統計データからデータ部取得
    data = json['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']
    #print('==================================================')
    #print(data)
    
    # jsonからDataFrameを作成
    values = data['VALUE']
    df = pd.DataFrame(values)
    #print('==================================================')
    #print(df)
    
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
    
    # 統計データのカテゴリ要素をID(数字の羅列)から、意味がわかる名称に変更する
    for class_obj in meta_info:
    
        # メタ情報の「@id」の先頭に'@'を付与'した文字列が、
        # 統計データの列名と対応している
        column_name = '@' + class_obj['@id']
        
        # 統計データの列名を「@code」から「@name」に置換するディクショナリを作成
        id_to_name_dict = {}
        for obj in class_obj['CLASS']:
            id_to_name_dict[obj['@code']] = obj['@name']
        
        # ディクショナリを用いて、指定した列の要素を置換 
        stats_data[column_name] = stats_data[column_name].replace(id_to_name_dict)
    
    # 統計データの列名を変換するためのディクショナリを作成
    col_replace_dict = {'@unit': '単位', '$': '値'}
    for class_obj in meta_info:
        org_col = '@' + class_obj['@id']
        new_col = class_obj['@name']
        col_replace_dict[org_col] = new_col
    
    # ディクショナリに従って、列名を置換する
    new_columns = []
    for col in stats_data:
        if col in col_replace_dict:
            new_columns.append(col_replace_dict[col])
        else:
            new_columns.append(col)
            
    stats_data.columns = new_columns
    
    print(stats_data)
