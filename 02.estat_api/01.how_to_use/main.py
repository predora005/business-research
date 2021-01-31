# coding: utf-8

import sys
import requests
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

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
    #print(url)
    
    # メタ情報取得
    json = requests.get(url).json()
    #print('==================================================')
    #print(json)
    
    # メタ情報から各表のデータ部取得
    class_objs = json['GET_META_INFO']['METADATA_INF']['CLASS_INF']['CLASS_OBJ']
    #print('==================================================')
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
    #print(url)
    
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
# 統計データのカテゴリ要素をID(数字の羅列)から、
# 意味がわかる名称に変更する
##################################################
def symbol_to_string(meta_info, stats_data):
    
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
    
    return stats_data
    
##################################################
# 出生率と死亡率を折れ線グラフ表示
##################################################
def plot_birth_and_mortality_rate(df):
    
    # 日本語フォントの設定
    mpl.font_manager._rebuild()    # キャッシュの削除
    plt.rcParams['font.family'] = 'IPAGothic'    # 日本語フォントを指定
    
    # 出生率と死亡率を取得する
    birth_rate = df[df['人口動態総覧'] == '出生率']
    mortality_rate = df[df['人口動態総覧'] == '死亡率']
    
    # 図と座標軸を取得
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    
    # 折れ線グラフをセット
    ax.plot(birth_rate['年度'], birth_rate['値'], label='出生率(人口千対)')
    ax.plot(mortality_rate['年度'], mortality_rate['値'], label='死亡率(人口千対)')
    ymax = max( [birth_rate['値'].max(), mortality_rate['値'].max()] )
    ax.set_ylim([0, ymax])
    ax.legend()
    
    # 折れ線グラフを表示
    fig.show()
    fig.savefig('birth_and_mortality_rate.png')
    
##################################################
# 出生率・死亡率・自然増減率を折れ線グラフ表示
##################################################
def plot_birth_mortality_natural_id_rate(df):
    
    # 日本語フォントの設定
    mpl.font_manager._rebuild()    # キャッシュの削除
    plt.rcParams['font.family'] = 'IPAGothic'    # 日本語フォントを指定
    
    # 出生率・死亡率・自然増減率を取得する
    birth_rate = df[df['人口動態総覧'] == '出生率']
    mortality_rate = df[df['人口動態総覧'] == '死亡率']
    natutal_id_rate = df[df['人口動態総覧'] == '自然増減率']
    
    # 図と座標軸を取得
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    
    # 出生率・死亡率を第一軸にプロット
    ax.plot(birth_rate['年度'], birth_rate['値'], label='出生率(人口千対)')
    ax.plot(mortality_rate['年度'], mortality_rate['値'], label='死亡率(人口千対)')
    ymax = max( [birth_rate['値'].max(), mortality_rate['値'].max()] )
    ax.set_ylim([0, ymax])
    ax.legend()
    
    # 自然増減率を第二軸にプロット
    ax2 = ax.twinx()
    ax2.plot(natutal_id_rate['年度'], natutal_id_rate['値'], 'C2', ls=':', label='自然増減率(人口千対)')
    ax2.set_ylabel('自然増減率(人口千対)')
    ax2.grid(axis='y', color='gray', ls=':')

    # 折れ線グラフを表示
    fig.show()
    fig.savefig('birth_mortality_natural_id_rate.png')
    
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
    stats_data = symbol_to_string(meta_info, stats_data)
    #print(stats_data)
    
    # 時間軸(年次)を整数に変換
    stats_data['年度'] = stats_data['時間軸(年次)'].map(lambda year: int(year.replace('年','')))

    # 有効値以外をNaNに置換する
    #   <NOTE char="***">調査又は集計していないもの</NOTE>
    #   <NOTE char="-">計数のない場合</NOTE>
    #   <NOTE char="・">統計項目のありえない場合</NOTE>
    #   <NOTE char="…">計数不明の場合</NOTE>
    stats_data['値'] = stats_data['値'].replace(['***', '-', '.', '…'], np.nan)
    stats_data['値'] = stats_data['値'].astype(np.float64)
     
    # 出生率と死亡率を折れ線グラフ表示
    plot_birth_and_mortality_rate(stats_data)
    
    # 出生率・死亡率・自然増減率を折れ線グラフ表示
    plot_birth_mortality_natural_id_rate(stats_data)
    