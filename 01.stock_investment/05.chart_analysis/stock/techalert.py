# coding: utf-8

import os
import csv
import pandas as pd
from stock.file import *
from stock.techind import *
from stock.s3 import *

##############################
# テクニカル指標分析によるアラートを出力する
##############################
def make_tech_alerts(dirpath, codes):
    
    # テクニカル指標分析のファイル名称を取得する
    filepath = get_tech_analyze_filename(dirpath)
    
    # ファイルが存在しない場合は作成する
    if not os.path.isfile(filepath):
        with open(filepath, 'w') as f:
            writer = csv.writer(f)
            header = ['']
            header.extend(__get_columns())
            writer.writerow(header)
    
    # テクニカル指標分析のファイルを読み込む
    df_analysis = pd.read_csv(filepath, header=0, index_col=0, parse_dates=[1])
        
    # 銘柄毎に分析を実施
    for code in codes:
        
        # 株価保存ファイルを読み込む
        df_value = read_stock_prices(dirpath, code)
        
        # テクニカル指標を追加する
        df_value = add_technical_indicators(df_value)
        
        # MACDの分析結果を追加
        df_analysis = analyze_macd(df_analysis, df_value, code)
        
        # MACDヒストグラムの分析結果を追加
        df_analysis = analyze_hist_5days(df_analysis, df_value, code)
        
        # RSIの分析結果を追加
        df_analysis = analyze_rsi(df_analysis, df_value, code)
        
    # 日付順にソートする
    df_analysis = df_analysis.sort_values(by=['Date', 'Code'], ignore_index=True)

    # CSVファイルに更新する
    df_analysis.to_csv(filepath)
    
    # 保存したファイルをS3にアップロードする
    s3_upload_analysis(dirpath)
    
##############################
# MACDを分析する(ゴールデンクロスとデッドクロス)
##############################
def analyze_macd(df_analysis, df_value, code):
    
    # ヒストグラムと日付を取り出す
    hists = df_value['Hist']
    dates = df_value.index
    
    # 空のリストを用意する
    add_rows = []
    
    # 行数分ループ
    for i in range(0, hists.size-1):
        
        # 2日分取り出し
        h1 = hists.iloc[i]
        h2 = hists.iloc[i+1]
        
        # ゴールデンクロス・デッドクロスを判定
        if h1 < 0 < h2:
            # ゴールデンクロス
            date = dates[i+1]
            details = f'{h1:.1f},{h2:.1f}'
            add_row = [date, code, ' MACD', 'ゴールデンクロス', details]
            add_rows.append(add_row)
            #print(f'{dates[i+1]:%Y-%m-%d} {code} ゴールデンクロス {h1:.1f},{h2:.1f}')
            
        elif h1 > 0 > h2:
            # デッドクロス
            date = dates[i+1]
            details = f'{h1:.1f},{h2:.1f}'
            add_row = [date, code, ' MACD', 'デッドクロス', details]
            add_rows.append(add_row)
            #print(f'{dates[i+1]:%Y-%m-%d} {code} デッドクロス {h1:.1f},{h2:.1f}')
            
    # 元のDataFrameに分析結果を追加する
    df_add_row = pd.DataFrame(add_rows, columns=__get_columns())
    df_analysis = df_analysis.append(df_add_row, ignore_index=True)
    
    return df_analysis
    
##############################
# MACDヒストグラムを分析する(3日間の上昇・減少で判定)
##############################
def analyze_hist_3days(df_analysis, df_value, code):
    
    # ヒストグラムと日付を取り出す
    hists = df_value['Hist']
    dates = df_value.index
    
    # 空のリストを用意する
    add_rows = []
    
    # 行数分ループ
    for i in range(0, hists.size-3):
        
        # 3日分取り出し
        h3d = hists.iloc[i:i+3]
        
        # 日毎の差分を取得
        hdiff = h3d.diff()
        
        # ボトムアウト・ピークアウトを判定
        if (hdiff[1] < 0 < hdiff[2]) and (h3d[1] < 0):
            # ボトムアウト
            date = dates[i+1]
            details = f'{h3d[0]:.1f},{h3d[1]:.1f},{h3d[2]:.1f}'
            add_row = [date, code, 'ヒスト', 'ボトムアウト', details]
            add_rows.append(add_row)
            hist_values = f'{h3d[0]:.1f},{h3d[1]:.1f},{h3d[2]:.1f}'
            #print(f'{dates[i+1]:%Y-%m-%d} {code} ボトムアウト {hist_values}')
            
        elif (hdiff[1] > 0 > hdiff[2]) and (h3d[1] > 0):
            # ピークアウト
            date = dates[i+1]
            details = f'{h3d[0]:.1f},{h3d[1]:.1f},{h3d[2]:.1f}'
            add_row = [date, code, 'ヒスト', 'ピークアウト', details]
            add_rows.append(add_row)
            hist_values = f'{h3d[0]:.1f},{h3d[1]:.1f},{h3d[2]:.1f}'
            #print(f'{dates[i+1]:%Y-%m-%d} {code} ピークアウト {hist_values}')
            
    # 元のDataFrameに分析結果を追加する
    df_add_row = pd.DataFrame(add_rows, columns=__get_columns())
    df_analysis = df_analysis.append(df_add_row, ignore_index=True)
    
    return df_analysis
    
##############################
# MACDヒストグラムを分析する(5日間の上昇・減少で判定)
##############################
def analyze_hist_5days(df_analysis, df_value, code):
    
    # ヒストグラムと日付を取り出す
    hists = df_value['Hist']
    dates = df_value.index
    
    # 空のリストを用意する
    add_rows = []
    
    # 行数分ループ
    for i in range(0, hists.size-5):
        
        # 5日分取り出し
        h5d = hists.iloc[i:i+5]
        
        # 日毎の差分を取得
        hdiff = h5d.diff()
        
        # ボトムアウト・ピークアウトを判定
        if (hdiff[1] < 0) and (hdiff[2] < 0) and \
            (hdiff[3] > 0) and (hdiff[4] > 0) and \
            (h5d[2] < 0):
            # ボトムアウト
            date = dates[i+2]
            details = f'{h5d[0]:.1f},{h5d[1]:.1f},{h5d[2]:.1f},{h5d[3]:.1f},{h5d[4]:.1f}'
            add_row = [date, code, 'ヒスト', 'ボトムアウト', details]
            add_rows.append(add_row)
            hist_values = f'{h5d[0]:.1f},{h5d[1]:.1f},{h5d[2]:.1f},{h5d[3]:.1f},{h5d[4]:.1f}'
            #print(f'{dates[i+2]:%Y-%m-%d} {code} ボトムアウト {hist_values}')
            
        elif (hdiff[1] > 0) and (hdiff[2] > 0) and \
            (hdiff[3] < 0) and (hdiff[4] < 0) and \
            (h5d[2] > 0):
            # ピークアウト
            date = dates[i+2]
            details = f'{h5d[0]:.1f},{h5d[1]:.1f},{h5d[2]:.1f},{h5d[3]:.1f},{h5d[4]:.1f}'
            add_row = [date, code, 'ヒスト', 'ピークアウト', details]
            add_rows.append(add_row)
            hist_values = f'{h5d[0]:.1f},{h5d[1]:.1f},{h5d[2]:.1f},{h5d[3]:.1f},{h5d[4]:.1f}'
            #print(f'{dates[i+2]:%Y-%m-%d} {code} ピークアウト {hist_values}')
            
    # 元のDataFrameに分析結果を追加する
    df_add_row = pd.DataFrame(add_rows, columns=__get_columns())
    df_analysis = df_analysis.append(df_add_row, ignore_index=True)
    
    return df_analysis
    
##############################
# RSIを分析する
##############################
def analyze_rsi(df_analysis, df_value, code):
    
    # 空のリストを用意する
    add_rows = []
    
    # 行数分ループ
    for i, rsi in enumerate(df_value['RSI']):
        
        if rsi > 70:
            # 売りシグナル
            date = df_value.index[i]
            details = f'{rsi:.1f}'
            add_row = [date, code, ' RSI', '70%以上', details]
            add_rows.append(add_row)
            #print(f'{df_value.index[i]} RSI>70% {rsi:.1f}')
        
        elif rsi < 30:
            # 買いシグナル
            date = df_value.index[i]
            details = f'{rsi:.1f}'
            add_row = [date, code, ' RSI', '30%以下', details]
            add_rows.append(add_row)
            #print(f'{df_value.index[i]} RSI<30% {rsi:.1f}')
    
    # 元のDataFrameに分析結果を追加する
    df_add_row = pd.DataFrame(add_rows, columns=__get_columns())
    df_analysis = df_analysis.append(df_add_row, ignore_index=True)
    
    return df_analysis
    
##############################
# CSVの出力項目(列)を取得する
##############################
def __get_columns():
    return ['Date', 'Code', 'Indicator', 'Alert', 'Details']
    