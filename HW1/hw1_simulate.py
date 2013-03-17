## CompInvesting I
## hw1_simulate.py
## HW1 - Implementation of the Simulate function

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

NUM_TRADING_DAYS = 252

def simulate( dt_start, dt_end, ls_symbols, ls_allocation ):
        # Formatting the date timestamps
        dt_timeofday = dt.timedelta(hours=16)
        ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

        # Open the dataset and read in the closing price
        ls_keys = ['close']
        c_dataobj = da.DataAccess('Yahoo')
        ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
        d_data = dict(zip(ls_keys, ldf_data))
        
        # Calculate the portfolio value
        temp = d_data['close'].values.copy()
        d_normal = temp / temp[0,:]
        alloc = np.array(ls_allocation).reshape(4,1)
        portVal = np.dot(d_normal, alloc)

        # Caluclate the daily returns
        dailyVal = portVal.copy()
        tsu.returnize0(dailyVal)

        # Calculate statistics
        daily_ret = np.mean(dailyVal)
        vol = np.std(dailyVal)
        sharpe = np.sqrt(NUM_TRADING_DAYS) * daily_ret / vol
        cum_ret = portVal[portVal.shape[0] -1][0]
        
        return vol, daily_ret, sharpe, cum_ret



def print_simulate( dt_start, dt_end, ls_symbols, ls_allocation ):
        vol, daily_ret, sharpe, cum_ret  = simulate( dt_start, dt_end, ls_symbols, ls_allocation )
        print "Start Date: ", dt_start
        print "End Date: ", dt_end
        print "Symbols: ", ls_symbols
        print "Optimal Allocations: ", ls_allocation
        print "Sharpe Ratio: ", sharpe
        print "Volatility (stdev): ", vol
        print "Average Daily Return: ", daily_ret
        print "Cumulative Return: ", cum_ret



def optimal_allocation_4( dt_start, dt_end, ls_symbols ):

        max_sharpe = -1
        max_alloc = [0.0, 0.0, 0.0, 0.0]
        for i in range(0,11):
                for j in range(0,11-i):
                        for k in range(0,11-i-j):
                                for l in range (0,11-i-j-k):
                                        if (i + j + l + k) == 10:
                                                alloc = [float(i)/10, float(j)/10, float(k)/10, float(l)/10]
                                                vol, daily_ret, sharpe, cum_ret = simulate( dt_start, dt_end, ls_symbols, alloc )
                                                if sharpe > max_sharpe:
                                                        max_sharpe = sharpe
                                                        max_alloc = alloc

        return max_alloc




# Example 1
dt_start = dt.datetime(2010,1,1)
dt_end = dt.datetime(2010,12,31)
ls_symbols = ['BRCM', 'TXN', 'AMD', 'ADI']
ls_allocation = [0.4, 0.4, 0.0, 0.2]

max_alloc = optimal_allocation_4( dt_start, dt_end, ls_symbols )
print_simulate( dt_start, dt_end, ls_symbols, max_alloc )

# Example 2
#dt_start = dt.datetime(2010,1,1)
#dt_end = dt.datetime(2010,12,31)
#ls_symbols = ['AXP', 'HPQ', 'IBM', 'HNZ']
#ls_allocation = [0.0, 0.0, 0.0, 1.0]

#max_alloc = optimal_allocation_4( dt_start, dt_end, ls_symbols )
#print_simulate( dt_start, dt_end, ls_symbols, ls_allocation )


