## Computational Investing I
## HW 5
##
## Author: alexcpsec

import pandas as pd
import pandas.stats.moments as pdsm
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep


def bollinger_bands(ldt_timestamps, ls_symbols, lookback):
    dataobj = da.DataAccess('Yahoo')
    
    ls_keys = ['close','actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method = 'ffill')
        d_data[s_key] = d_data[s_key].fillna(method = 'bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    df_close = d_data['close']
    df_mean = pd.rolling_mean(df_close, lookback)
    df_std = pd.rolling_std(df_close, lookback)

    df_bands = (df_close - df_mean) / df_std
    

  
if __name__ == '__main__':
    dt_start = dt.datetime(2010, 1, 1)
    dt_end = dt.datetime(2010, 12, 31)
    ls_symbols = ["AAPL", "GOOG", "IBM", "MSFT"]
    lookback = 20
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    ## Starting up with SP500 2008
    bollinger_bands(ldt_timestamps, ls_symbols, lookback)

