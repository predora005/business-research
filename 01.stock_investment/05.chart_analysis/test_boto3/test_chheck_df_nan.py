# coding: utf-8

import numpy as np
import pandas as pd

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    list1 = [1, 2, 3]
    list2 = [np.nan, np.nan, np.nan, ]
    
    df = pd.DataFrame({'1': list1, '2': list2})
    #print(df)
    
    # 列がすべてNaNか?
    isnull_columns = df.isnull().all()
    print(isnull_columns)
    print(type(isnull_columns))
    
    # すべてNaNの列は存在するか?
    has_nan_column = isnull_columns.any()
    print(has_nan_column)
    
    