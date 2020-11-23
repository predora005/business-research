# coding: utf-8

import os
import datetime
import time
from stinfo import *

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    codes = {
        'JR東日本'  : 9020, 
        'JR西日本'  : 9022, 
        'JR東海'    : 9021, 
        '東急'      : 9005, 
        '近鉄GHD'   : 9041,
    }
    
    df = get_basic_infos(codes)
    print(df)
    
    #for code in codes:
    #    basic_info = get_basic_info(code)
    #    print(basic_info)
    #    
    #    # 1秒ディレイ
    #    time.sleep(1)
        
    
    