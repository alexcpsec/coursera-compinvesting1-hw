## Computational Investing I
## HW 4
##
## Author: alexcpsec

import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep

"""
Accepts a list of symbols along with start and end date
Returns the Event Matrix which is a pandas Datamatrix
Event matrix has the following structure :
    |IBM |GOOG|XOM |MSFT| GS | JP |
(d1)|nan |nan | 1  |nan |nan | 1  |
(d2)|nan | 1  |nan |nan |nan |nan |
(d3)| 1  |nan | 1  |nan | 1  |nan |
(d4)|nan |  1 |nan | 1  |nan |nan |
...................................
...................................
Also, d1 = start date
nan = no information about any event.
1 = status bit(positively confirms the event occurence)
"""

evtAmount = 6.0
orderFile = "order_h4-6.csv"
strSymbols =  "sp5002012"

def find_events(ls_symbols, d_data, event_amount):
    df_close = d_data['actual_close']

    print "Finding Events..."

    # Creating an empty dataframe
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_close.index

    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            # Calculating the returns for this timestamp
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
            
            if f_symprice_yest >= event_amount and f_symprice_today < event_amount:
                df_events[s_sym].ix[ldt_timestamps[i]] = 1

    return df_events

def create_orders_events(ldt_timestamps, symbols_list, event_amount):
    dataobj = da.DataAccess('Yahoo')
    ls_symbols = dataobj.get_symbols_from_list(symbols_list)
    ls_symbols.append('SPY')

    ls_keys = ['close','actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method = 'ffill')
        d_data[s_key] = d_data[s_key].fillna(method = 'bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    df_events = find_events(ls_symbols, d_data, event_amount)

    file_out = open( orderFile, "w" )

    for col in df_events.columns:
        for i in range(0,len(ldt_timestamps)):
            date = ldt_timestamps[i]
            if not np.isnan(df_events.get_value(date,col)):
                if i+5 >= len(ldt_timestamps):
                    date2 = ldt_timestamps[len(ldt_timestamps) - 1]
                else:
                    date2 = ldt_timestamps[i+5]
                file_out.writelines(date.strftime('%Y,%m,%d') + "," + str(col) + ",Buy,100\n")
                file_out.writelines(date2.strftime('%Y,%m,%d') + "," + str(col) + ",Sell,100\n")

    file_out.close()

                

if __name__ == '__main__':
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    ## Starting up with SP500 2008
    create_orders_events(ldt_timestamps, strSymbols, evtAmount)
