# coding: utf-8

import matplotlib as mpl
import matplotlib.pyplot as plt

##############################
#  matplotlibのフォント設定処理
##############################
def plt_font_init():
    
    # 日本語フォントの設定
    mpl.font_manager._rebuild()    # キャッシュの削除
    plt.rcParams['font.family'] = 'IPAGothic'    # 日本語フォントを指定

