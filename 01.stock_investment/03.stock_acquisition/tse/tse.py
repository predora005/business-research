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
# 東証銘柄の業界ごと株価上昇率を取得する
##############################
def get_tse_increase_rate_by_industry(tse, base_date):
    
    # 33業種コード,33業種区分を抽出
    industry_category = tse.groupby(['33業種コード','33業種区分']).groups.keys()
    industry_category = [keys[1] for keys in industry_category]
    #print("==================================================")
    #print(industry_category)
    
    # 33業種コードでソートしたいので上記処理に変更
    #industry_category = tse['33業種区分'].unique()
    #industry_category.sort()

    # 株価上昇率格納用のDataFrameを用意する
    df = None
    
    # 業種ごとに変動率を計算する
    for category in industry_category:
        
        #print("==================================================")
        #print(category)
        
        # 指定した業種の銘柄を抽出
        brands = tse[tse['33業種区分'] == category]
        
        #print("==================================================")
        #print(brands)
        
        # 銘柄コードの末尾に.JPを付加する
        symbols = []
        for code in brands['コード']:
            symbols.append('{0:d}.JP'.format(code))
        
        # 指定銘柄コードの株価を取得する
        stock_price = web.DataReader(symbols, 'stooq', start=base_date)
        
        #print("==================================================")
        #print(stock_price)
        
        # 銘柄ごとに上昇率を計算し、ディショクナリに格納する
        dict = {}
        for symbol in symbols:
            
            #print("==================================================")
            #print(symbol)
            
            # 銘柄ごとに上昇率を計算し、ディショクナリに格納する
            # 基準日付からの上昇率を計算する
            base_date_str = base_date.strftime('%04Y-%02m-%02d')
            base_price = stock_price.loc[base_date_str][('Close',symbol)]
            increase_rate = stock_price[('Close',symbol)] / base_price.iloc[0]
            
            # ディクショナリに格納する
            dict[symbol] = increase_rate
            
        # 各銘柄の上昇率の平均値を計算する
        category_df = pd.DataFrame(dict)
        mean = category_df.mean(axis='columns')
        std = category_df.std(axis='columns')
        
        print("==================================================")
        print(category_df)
        
        # DataFrameに上昇率と、上昇率の標準偏差を格納する
        if df is None:
            df = pd.concat([mean, std], axis=1)
            df.columns = pd.MultiIndex.from_tuples([(category, '上昇率'), (category, '標準偏差')])
        else:
            df[(category, '上昇率')] = mean
            df[(category, '標準偏差')] = std
            
        print("==================================================")
        print(df)
        
    return df
    
