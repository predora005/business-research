# coding: utf-8

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
    
