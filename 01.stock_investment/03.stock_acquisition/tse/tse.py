# coding: utf-8

#import numpy as np
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt

##############################
# 東証上場銘柄一覧を取得
##############################
def get_tse_brand_list(filepath):
    
    df = pd.read_csv(filepath, header=0)
    
    return df
    
##############################
# 東証一部銘柄の業界ごと株価上昇率を取得する
##############################
def get_tse1_increase_rate_by_industry(brand_list, base_date):
    
    # 東証一部の銘柄を抽出
    tse1 = brand_list[brand_list['市場・商品区分'] == '市場第一部（内国株）']
    
    # 33業種コード,33業種区分を抽出
    #industry_category = tse1.groupby(['33業種コード','33業種区分']).groups.keys()
    industry_category = tse1['33業種区分'].unique()
    
    # 変動率格納用のDataFrameを用意する
    #df = pd.DataFrame(industry_category, columns=['33業種コード','33業種区分'])
    #df['変動率'] = 0
    df = None
    
    # 業種ごとに変動率を計算する
    #categories = df['33業種コード'].unique()
    #for category in categories:
        
    for category in industry_category:
        
        print(category)
        
        # 指定した業種の銘柄を抽出
        #brands = tse1[tse1['33業種コード'] == category]
        brands = tse1[tse1['33業種区分'] == category]
        
        # 銘柄ごとに上昇率を計算し、ディショクナリに格納する
        dict = {}
        for code in brands['コード']:
            print(code)
            
            # 指定銘柄の株価取得
            symbol ='{0:d}.JP'.format(code)
            stock_price = web.DataReader(symbol, 'stooq', start=base_date)
            print(stock_price)
            
            # 基準日付からの上昇率を計算する
            base_date_str = base_date.strftime('%04Y-%02m-%02d')
            base_price = stock_price.loc[base_date_str]['Close']
            increase_rate = stock_price['Close'] / base_price.iloc[0]
            
            # ディクショナリに格納する
            dict[code] = increase_rate
        
        # 各銘柄の上昇率の平均値を計算する
        category_df = pd.DataFrame(dict)
        mean = category_df.mean(axis='columns')
        std = category_df.std(axis='columns')
        
        # DataFrameに上昇率と、上昇率の標準偏差を格納する
        if df is None:
            df = pd.concat([mean, std], axis=1)
            df.columns = pd.MultiIndex.from_tuples([(category, '上昇率'), (category, '標準偏差')])
        else:
            df[(category, '上昇率')] = mean
            df[(category, '標準偏差')] = std
            
        #print(df)
        
        
    return df
    
