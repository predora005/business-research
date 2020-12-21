# coding: utf-8

import os
from stinfo import plt_font_init
from analyzer import RailroadAnalyzer,TwoWheeledVehicleAnalyzer

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    # matplotlibの日本語フォント設定
    plt_font_init()
    
    # ベースディレクトリをセット
    base_dir = os.getcwd()

    # 二輪車のアナライザを生成
    analyzer = TwoWheeledVehicleAnalyzer(base_dir, 'two_wheeled_vehicle')
    
    ## 鉄道のアナライザを生成
    #analyzer = RailroadAnalyzer(base_dir, 'railroad')
    
    # アナライザを実行する
    analyzer.run()
    
