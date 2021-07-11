# coding: utf-8

##############################
# テクニカル指標を追加する
##############################
def add_technical_indicators(df):
    
    # 日付で昇順ソース
    df_sort = df.sort_index()
    
    # MACDを追加
    df_macd = add_macd(df_sort)
    
    # RSIを追加
    df_rsi = add_rsi(df_macd)
    
    return df_rsi
    
##############################
# MACDとシグナルを追加する
##############################
def add_macd(df, start_date=None, end_date=None):
    
    #  終値
    close = df['Close']
    
    # 短期平均と長期平均
    exp12 = close.ewm(span=12, adjust=False).mean()
    exp26 = close.ewm(span=26, adjust=False).mean()
    
    # MACD
    df['MACD'] = exp12 - exp26
    
    # シグナル
    df['Signal'] = df['MACD'].rolling(window=9).mean()
    
    # ヒストグラム(MACD-シグナル)
    df['Hist'] = df['MACD'] - df['Signal']
    
    return df
    
##############################
# RSIを追加する
##############################
def add_rsi(df, start_date=None, end_date=None):
    
    # 株価の差分
    df_diff = df['Close'].diff()
    #print('==========')
    #print(df_diff)
    
    # 値上がり幅と値下がり幅を取得
    df_up, df_down = df_diff.copy(), df_diff.copy()
    df_up[df_up < 0] = 0
    df_down[df_down > 0] = 0
    df_down = df_down * -1
    
    # 14日間の単純移動平均
    sim14_up = df_up.rolling(window=14).mean()
    sim14_down = df_down.rolling(window=14).mean()

    # RSI
    df['RSI'] = sim14_up / (sim14_up + sim14_down) * 100
    
    return df
    
