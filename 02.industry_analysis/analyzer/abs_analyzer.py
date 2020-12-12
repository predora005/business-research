# coding: utf-8

from abc import ABCMeta, abstractmethod
import os
from stinfo import *

##################################################
# 解析クラスの基底クラス
##################################################
class AbsAnalyzer(metaclass=ABCMeta):
    """データロードクラスの基底クラス
        
    Attributes:
        _base_dir (string)      : ベースディレクトリ
        _ouput_dirname (string) : 出力ディレクトリ名
        _ouput_dir (string)     : 出力ディレクトリパス
    """

    ##################################################
    # コンストラクタ
    ##################################################
    def __init__(self, base_dir, ouput_dirname):
        """ コンストラクタ。
        
        Args:
            base_dir (string)       : ベースディレクトリ
            ouput_dirname (string)  : 出力ディレクトリ名
        Returns:
        """
        
        self._base_dir = base_dir
        self._ouput_dirname = ouput_dirname
    
        # 出力用ディレクトリをセットする
        self._ouput_dir = os.path.join(self._base_dir, self._ouput_dirname)
        
        # 出力用ディレクトリを作成する
        os.makedirs(self._ouput_dir, exist_ok=True)
        
    ##################################################
    # 解析を実行する。
    ##################################################
    def  run(self):
        """ 解析を実行する。
        
        Args:
            
        Returns:
        """
        
        # 証券コードと名称のディクショナリを取得する
        codes = self.get_codes()
        
        # 各銘柄の基本情報を解析する。
        self.analyze_basic_infos(codes)
        
        
    ##################################################
    # 各銘柄の基本情報を取得する。
    ##################################################
    def  analyze_basic_infos(self, codes):
        """ 各銘柄の基本情報を取得する。
        
        Args:
            codes   (dict)  : 証券コードと名称のディクショナリ
                              (ex){'JR東日本':9020, 'JR西日本': 9021}
        Returns:
        """
        
        # 各銘柄の基本情報を取得する。
        df = get_basic_infos(codes)
        
        # 各銘柄の基本情報を整形する。
        df = reshape_basic_info(df)
        
        # 平均値と標準偏差の列を削除する
        df = df.drop(index='標準偏差')
        df = df.drop(index='平均値')
        
        # PER,を可視化する。
        per_file = os.path.join(self._ouput_dir, 'per.png')
        visualize_basic_info(df, ['PER(調整後)'], per_file)
        
        # PER, PBR, PSRを可視化する。
        psr_pbr_file = os.path.join(self._ouput_dir, 'psr_pbr.png')
        visualize_basic_info(df, ['PSR', 'PBR'], psr_pbr_file)
        
        # 時価総額を可視化する。
        market_cap_file = os.path.join(self._ouput_dir, 'market_cap.png')
        visualize_basic_info(df, ['時価総額(兆円)'], market_cap_file)
        
        # 配当利回りを可視化する
        dividend_yield_file = os.path.join(self._ouput_dir, 'dividend_yield.png')
        visualize_basic_info(df, ['配当利回り'], dividend_yield_file)
        
    ##################################################
    # 証券コードと名称のディクショナリを返す。
    ##################################################
    @abstractmethod
    def get_codes(self):
        """ 証券コードと名称のディクショナリを返す。
        
        Args:
        Returns:
            dict    : 証券コードと名称のディクショナリ
                        (ex){'JR東日本':9020, 'JR西日本': 9021}
        """
        raise NotImplementedError()
    