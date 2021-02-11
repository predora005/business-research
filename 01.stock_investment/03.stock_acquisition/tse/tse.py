# coding: utf-8

import numpy as np
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates
import datetime

##############################
# 東証上場銘柄一覧を取得
##############################
def get_tse_brand_list(filepath):
    
    df = pd.read_csv(filepath, header=0)
    
    return df
    
##############################
# 東証銘柄の業界ごと株価上昇率を取得する
##############################
def get_tse_increase_rate_by_industry(tse, base_date, end_date=None):
    
    # 33業種コード,33業種区分を抽出
    industry_category = tse.groupby(['33業種コード','33業種区分']).groups.keys()
    #print("==================================================")
    #print(industry_category)
    
    # 33業種コードでソートしたいので上記処理に変更
    #industry_category = tse['33業種区分'].unique()
    #industry_category.sort()
    
    # 業種単位の株価上昇率格納用のDataFrameを用意する
    category_df = None
    
    # 銘柄単位の株価上昇率格納用のディクショナリを用意する
    brand_dict = {}
    brand_count = 0
    
    # 業種ごとに変動率を計算する
    for category in industry_category:
        
        category_code = category[0]     # 33業種コード
        category_class = category[1]    # 33業種区分
        
        # 指定した業種の銘柄を抽出
        brands = tse[tse['33業種区分'] == category_class]
        
        #print("==================================================")
        print(category_code, category_class)
        #print(brands)
        
        # 銘柄コードの末尾に.JPを付加する
        symbols = []
        for code in brands['コード']:
            symbols.append('{0:d}.JP'.format(code))
            
        #print("==================================================")
        #print(symbols)
            
        # 指定銘柄コードの株価を取得する
        stock_price = web.DataReader(symbols, 'stooq', start=base_date, end=end_date)
        
        #print("==================================================")
        #print(stock_price)
        
        # 銘柄ごとに上昇率を計算し、ディショクナリに格納する
        dict = {}
        for symbol in symbols:
            
            # 銘柄ごとに上昇率を計算し、ディショクナリに格納する
            # 基準日付からの上昇率を計算する
            base_date_str = base_date.strftime('%04Y-%02m-%02d')
            base_price = stock_price.loc[base_date_str][('Close',symbol)]
            increase_rate = stock_price[('Close',symbol)] / base_price.iloc[0]

            # ディクショナリに格納する
            dict[symbol] = increase_rate
            
        # 業種内銘柄の上昇率の平均値を計算する
        df = pd.DataFrame(dict)
        mean = df.mean(axis='columns')
        std = df.std(axis='columns')
        
        #print("==================================================")
        #print(df)
        
        # DataFrameに業種単位の上昇率と、上昇率の標準偏差を格納する
        if category_df is None:
            category_df = pd.concat([mean, std], axis=1)
            category_df.columns = pd.MultiIndex.from_tuples(
                [(category_class, '上昇率'), (category_class, '標準偏差')])
        else:
            category_df[(category_class, '上昇率')] = mean
            category_df[(category_class, '標準偏差')] = std
            
        #print("==================================================")
        #print(category_df)
        
        # 最新の日付を取得する
        latest_date = df.index.max()
        latest_date_str = latest_date.strftime('%04Y-%02m-%02d')
        #print(latest_date_str)
        
        # 銘柄単位の株価上昇率をディクショナリに格納する
        for i, symbol in enumerate(symbols):
            
            code = brands['コード'].iloc[i]
            name = brands['銘柄名'].iloc[i]
            increase_rate = df.loc[latest_date_str, symbol].iloc[0]
            
            # '33業種コード','33業種区分', 'コード', '銘柄名', '上昇率'])
            brand_dict[brand_count] = [category_code, category_class, code, name, increase_rate]
            brand_count += 1
            
        #print("==================================================")
        #print(brand_dict)
        
    # 銘柄単位の株価上昇率を格納したDataFrameを作成する
    brand_df = pd.DataFrame.from_dict(
                    brand_dict, orient="index", 
                    columns=['33業種コード','33業種区分', 'コード', '銘柄名', '上昇率'])
    
    return category_df, brand_df
    
##############################
# 東証銘柄の業界ごと株価上昇率を折れ線グラフで表示する
##############################
def visualize_tse_increase_rate_by_industry_in_line(category_df, filepath=None):
    
    # 上昇率のみを抽出し、業種の数を取得する
    increase_rate_df = category_df.loc[:, pd.IndexSlice[:, '上昇率']]
    industry_num = len(increase_rate_df.columns)
    
    # figsize, rows, colsを取得し、Figureを取得
    figsize, rows, cols = get_subplot_size(industry_num)
    fig = plt.figure(figsize=figsize)
    
    # 月数を算出
    #min_date = increase_rate_df.index.min()
    #max_date = increase_rate_df.index.max()
    #min_x = datetime.date(min_date.year, min_date.month, 1)
    #max_x = datetime.date(max_date.year, max_date.month + 1, 1)
    #month_num = (max_x.year - min_x.year)*12 + max_x.month - min_x.month + 1
    
    # 上昇率の最大値と最小値を取得
    min_y = increase_rate_df.min().min()
    max_y = increase_rate_df.max().max()

    # 業種ごとに折れ線グラフを表示する
    for i in range(industry_num):
        
        # Axesを取得
        ax = fig.add_subplot(rows, cols, i+1)
        
        # 銘柄名
        category_name = increase_rate_df.columns[i][0]
        
        # 上昇率を取得
        increate_rate = increase_rate_df.loc[:, pd.IndexSlice[category_name, '上昇率']]
        
        # 表示するデータを抽出
        x = increase_rate_df.index
        y = increate_rate
        
        # 折れ線グラフを表示
        ax.plot(x, y, label=category_name)
        
        # 目盛り線を表示
        ax.grid(color='gray', linestyle='--', linewidth=0.5)
        
        # Y軸の単位をパーセント表示に設定
        #ax.yaxis.set_major_formatter(mpl.ticker.PercentFormatter(1))
        
        # X軸の目盛り位置を設定
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        #ax.xaxis.set_major_locator(mpl.ticker.LinearLocator(month_num))
        
        # X軸の表示フォーマットを設定
        #ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        
        # X軸とY軸の範囲を設定
        #ax.set_xlim(min_x, max_x) 
        ax.set_ylim(min_y, max_y) 
        
        # グラフのタイトルを追加
        ax.set_title(category_name)
        
    # 不要な余白を削る
    plt.tight_layout()
    
    # グラフを表示
    #fig.show()
    
    # グラフをファイルに出力
    if filepath is not None:
        fig.savefig(filepath)  
    
    # グラフを閉じる
    plt.close()

##############################
# 東証銘柄の業界ごと株価上昇率を棒グラフで表示する
##############################
def visualize_tse_increase_rate_by_industry_in_bar(category_df, filepath=None):
    
    # 最新日付を取得する
    latest_date = category_df.index.max()
    latest_date_str = latest_date.strftime('%04Y-%02m-%02d')
    
    # 最新日付の上昇率, 標準偏差を抽出する
    increase_rate = category_df.loc[latest_date_str, pd.IndexSlice[:, '上昇率']]
    std = category_df.loc[latest_date_str, pd.IndexSlice[:, '標準偏差']]
    
    # 業種名をリストで取得
    categories= [col[0] for col in increase_rate.columns]
    
    # 上昇率と標準偏差を列にもつDataFrameを作成し、
    # 上昇率で降順ソートする
    df = pd.DataFrame({'上昇率': increase_rate.values[0], '標準偏差': std.values[0]}, 
                        index=categories)
    df = df.sort_values('上昇率', ascending=False)
    print(df)
    
    # 図と座標軸を取得
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1,1,1)
    
    # 棒グラフに表示するデータを準備
    x = np.arange(len(categories))
    y = df['上昇率']
    yerr = df['標準偏差']
    
    # 棒グラフ表示
    ax.barh(x, y, xerr=yerr, tick_label=categories)
    
    # 目盛り線を表示
    ax.grid(axis='x', color='gray', linestyle='--', linewidth=0.5)
    
    # 不要な余白を削る
    plt.tight_layout()
    
    # グラフを表示
    #fig.show()
    
    # グラフをファイルに出力
    if filepath is not None:
        fig.savefig(filepath)  
    
    # グラフを閉じる
    plt.close()
    
##############################
# 東証銘柄の銘柄ごと株価上昇率の上位を取得する
##############################
def get_tse_top_increase_rate_by_brands(brand_df, top_num=5, bottom=False):
    
    # 上昇率でソート
    df_sorted = brand_df.sort_values('上昇率', ascending=bottom)
    
    # 上位銘柄を抽出
    df_top = df_sorted.head(top_num)
    
    return df_top
    
##################################################
# 複数グラフ表示する際の各種サイズを返す
##################################################
def get_subplot_size(plot_num):
    """ 複数グラフ表示する際の各種サイズを返す
    
    Args:
        plot_num     (int)  : 表示するグラフの個数

    Returns:
        figsize, rows, cols (int)
    """
    
    # サブプロットの行数・列数を決定
    if plot_num == 1:
        rows, cols = (1, 1)
        figsize=(6, 4)
    elif plot_num == 2:
        rows, cols = (1, 2)
        figsize=(10, 4)
    elif plot_num == 3:
        rows, cols = (1, 3)
        figsize=(15, 4)
    elif plot_num == 4:
        rows, cols = (2, 2)
        figsize=(10, 8)
    elif plot_num <= 6:
        rows, cols = (2, 3)
        figsize=(15, 8)
    elif plot_num <= 9:
        rows, cols = (3, 3)
        figsize=(15, 12)
    elif plot_num <= 16:
        rows, cols = (4, 4)
        figsize=(15, 12)
    elif plot_num <= 25:
        rows, cols = (5, 5)
        figsize=(20, 16)
    elif plot_num <= 36:
        rows, cols = (6, 6)
        figsize=(20, 16)
    else:
        rows, cols = (7, 7)
        figsize=(25, 24)
        
        
    return figsize, rows, cols
    