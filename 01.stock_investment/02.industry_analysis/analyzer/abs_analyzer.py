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
        codes = self._get_codes()
        
        # 各銘柄の基本情報を解析する。
        self._analyze_basic_infos(codes)
        
        # 各銘柄の決算情報を解析する。
        self._analyze_financial_infos(codes)
        
        # 各銘柄の株価を解析する。
        self._analyze_stock_pricess(codes)
        
    ##################################################
    # 各銘柄の基本情報を取得する。
    ##################################################
    def _analyze_basic_infos(self, codes):
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
        
        # PBR, PSRを可視化する。
        psr_pbr_file = os.path.join(self._ouput_dir, 'psr_pbr.png')
        visualize_basic_info(df, ['PSR', 'PBR'], psr_pbr_file)
        
        # 時価総額を可視化する。
        market_cap_file = os.path.join(self._ouput_dir, 'market_cap.png')
        visualize_basic_info(df, ['時価総額(兆円)'], market_cap_file)
        
        # 配当利回りを可視化する
        dividend_yield_file = os.path.join(self._ouput_dir, 'dividend_yield.png')
        visualize_basic_info(df, ['配当利回り'], dividend_yield_file)
        
    ##################################################
    # 各銘柄の決算情報を取得する。
    ##################################################
    def _analyze_financial_infos(self, codes):
        """ 各銘柄の決算情報を取得する。
        
        Args:
            codes   (dict)  : 証券コードと名称のディクショナリ
                              (ex){'JR東日本':9020, 'JR西日本': 9021}
        Returns:
        """
        
        # 指定した複数銘柄の基本情報を取得する。
        df = get_financial_infos(codes)
        
        # 複数銘柄の決算情報を整形する
        df = reshape_financial_info(df)
        
        # 各銘柄別に可視化する
        for brand_name in codes.keys():
            
            # 銘柄用のフォルダを作成
            code = codes[brand_name]
            dir_name = '{0:d}_{1:s}'.format(code, brand_name)
            brand_dir = os.path.join(self._ouput_dir, dir_name)
            os.makedirs(brand_dir, exist_ok=True)
            
            # ROAとROEを可視化する
            roa_roe_file = os.path.join(brand_dir, 'roa_roe.png')
            visualize_financial_info_for_specified_brand(
                df, brand_name, bar_datas=['ROA', 'ROE'], bar_label='ROA,ROE[%]', 
                filepath=roa_roe_file)
            
            # 利益を可視化する
            income_file = os.path.join(brand_dir, 'income.png')
            visualize_financial_info_for_specified_brand(
                df, brand_name, 
                bar_datas=['営業利益(十億円)', '経常利益(十億円)', '純利益(十億円)'], 
                bar_label='利益(十億円)',
                line_datas=['売上高(十億円)'], line_label='売上高(十億円)',
                filepath=income_file)
            
            # 資産を可視化する
            assets_file = os.path.join(brand_dir, 'assets.png')
            visualize_financial_info_for_specified_brand(
                df, brand_name, 
                bar_datas=['総資産(十億円)', '純資産(十億円)'], bar_label='資産(十億円)',
                line_datas=['純利益(十億円)'], line_label='利益(十億円)',
                filepath=assets_file)
            
            # キャッシュフロー情報を可視化する
            cf_file = os.path.join(brand_dir, 'cf.png')
            visualize_financial_info_for_specified_brand(
                df, brand_name, 
                bar_datas=['営業CF(十億円)', '投資CF(十億円)', '財務CF(十億円)', '現金期末残高(十億円)'], 
                bar_label='キャッシュ(十億円)',
                filepath=cf_file)
            
    ##################################################
    # 各銘柄の株価を解析する。
    ##################################################
    def _analyze_stock_pricess(self, codes):
        """ 各銘柄の株価を解析する。
        
        Args:
            codes   (dict)  : 証券コードと名称のディクショナリ
                              (ex){'JR東日本':9020, 'JR西日本': 9021}
        Returns:
        """
        
        # 株価取得の範囲(開始年, 終了年)を取得する
        start_year, end_year = self._get_date_range_for_stock_price()
        
        # 指定した複数銘柄の株価を取得する
        df = get_stock_prices(codes, start_year, end_year)
        
        # 株価を補正する
        df = self._correct_stock_prices(df)
        
        # 銘柄名を取得する
        brand_names = list(df.index.unique('銘柄'))
        
        # 複数銘柄の値上がり率を折れ線グラフで可視化する
        ref_date = self._get_ref_date_for_price_rates()
        price_rate_file = os.path.join(self._ouput_dir, 'stock_price_rate.png')
        visualize_stock_price_rates_in_line(df, brand_names, ref_date=ref_date, filepath=price_rate_file)
        
        # 複数銘柄の株価を折れ線グラフで可視化する
        start_date = self._get_stock_chart_start_date()
        df2 = df.loc[pd.IndexSlice[:, start_date:], :]
        stock_chart_file = os.path.join(self._ouput_dir, 'stock_chart.png')
        visualize_multi_stock_prices_in_line(df2, brand_names, show_average=True, filepath=stock_chart_file)
        
    ##################################################
    # 証券コードと名称のディクショナリを返す。
    ##################################################
    @abstractmethod
    def _get_codes(self):
        """ 証券コードと名称のディクショナリを返す。
        
        Args:
        Returns:
            dict    : 証券コードと名称のディクショナリ
                        (ex){'JR東日本':9020, 'JR西日本': 9021}
        """
        raise NotImplementedError()
    
    ##################################################
    # 株価取得の範囲(開始年, 終了年)を取得する
    ##################################################
    @abstractmethod
    def _get_date_range_for_stock_price(self):
        """ 株価取得の範囲(開始年, 終了年)を取得する
        
        Args:
        Returns:
            tuple   : 開始年, 終了年
        """
        raise NotImplementedError()
    
    ##################################################
    # 値上がり率の基準とする日付を取得する。
    ##################################################
    @abstractmethod
    def _get_ref_date_for_price_rates(self):
        """ 値上がり率の基準とする日付を取得する。
        
        Args:
        Returns:
            datetime    : 値上がり率の基準とする日付
        """
        raise NotImplementedError()
    
    ##################################################
    # 株価チャート表示開始日付を取得する。
    ##################################################
    @abstractmethod
    def _get_stock_chart_start_date(self):
        """ 株価チャート表示開始日付を取得する。
        
        Args:
        Returns:
            string  : 株価チャート表示開始日付を下記形式の文字列で返す。
                        (ex) 'YYYY-MM-DD'
        """
        raise NotImplementedError()
        
    ##################################################
    # 株価を補正する。
    ##################################################
    @abstractmethod
    def _correct_stock_prices(self, df):
        """ 株価を補正する。
            株式分割や併合に対する補正として使用する。
        Args:
            df(DataFrame)   : 株価データが格納されたDataFrame
        Returns:
            DataFrame   : 補正後のDataFrame
        """
        return df
        