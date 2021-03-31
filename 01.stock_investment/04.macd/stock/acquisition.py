# coding: utf-8

#import numpy as np
#import pandas as pd
import pandas_datareader.data as web
#import matplotlib.pyplot as plt
#import matplotlib as mpl
#import matplotlib.dates as mdates
#import datetime

##############################
# 指定した銘柄コードの株価を取得する
##############################
def get_stock_prices(code, start_date, end_date=None):

    # 指定銘柄コードの株価を取得する
    stock_prices = web.DataReader(code, 'stooq', start=start_date, end=end_date)
        
    return stock_prices
    