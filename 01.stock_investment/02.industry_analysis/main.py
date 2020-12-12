# coding: utf-8

import os
from stinfo import plt_font_init
from analyzer import RailroadAnalyzer

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    # matplotlibの日本語フォント設定
    plt_font_init()
    
    # ベースディレクトリをセット
    base_dir = os.getcwd()

    # 鉄道のアナライザを生成
    railroad_analyzer = RailroadAnalyzer(base_dir, 'railroad')
    
    # アナライザを実行する
    railroad_analyzer.run()
    
    