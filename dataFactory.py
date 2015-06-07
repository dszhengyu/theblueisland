from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas.tseries.offsets import Day
import matplotlib.pyplot as plt

pwd = 'z:\\theblueisland\\'
raw_data = pwd + 'raw_data\\'
user_balance_table = raw_data + 'user_balance_table.csv'
user_balance_table_parsed_date = raw_data + 'user_balance_table_parsed_date.csv'
user_balance_table_clean = raw_data + 'user_balance_table_clean.csv'
user_profile_table = raw_data + 'user_profile_table.csv'
day_share_interest_table = raw_data + 'mfd_day_share_interest.csv'
mfd_bank_shibor_table = raw_data + 'mfd_bank_shibor.csv'

## first time, parse date
# user_balance = pd.read_csv(user_balance_table, parse_dates = ['report_date'])
# user_balance.fillna(0, inplace = True)
# user_balance.to_csv(user_balance_table_parsed_date, index = None)


## global data member
user_balance = pd.read_csv(user_balance_table_parsed_date, parse_dates = ['report_date'])
# clean data here
userGroup = user_balance.groupby('user_id')
pLess10 = userGroup['total_purchase_amt'].max() < 10
rLess10 = userGroup['total_redeem_amt'].max() < 10
less10 = np.logical_and(pLess10, rLess10)
toKeep = less10[less10 == False]
user_balance_clean = user_balance.set_index('user_id')
user_balance_clean = user_balance_clean.ix[toKeep.index]
user_balance_clean.reset_index(inplace = True)
user_balance_clean.to_csv(user_balance_table_clean)

## generate data
def get_user_balance():
    global user_balance
    return user_balance
    
def get_user_balance_clean():
    global user_balance_clean
    return user_balance_clean
    
def get_day_share_interest():
    day_share_interest = pd.read_csv(day_share_interest_table, parse_dates = ['mfd_date'],
                                        index_col = 'mfd_date')
    return day_share_interest

def get_mfd_bank_shibor():
    mfd_bank_shibor = pd.read_csv(mfd_bank_shibor_table, parse_dates = ['mfd_date'])
    mfd_bank_shibor.ix[295, 'mfd_date'] = datetime(2014, 8, 31)
    mfd_bank_shibor.ix[294, 'mfd_date'] = datetime(2014, 8, 30)
    mfd_bank_shibor.fillna(method = 'ffill', inplace = True)
    mfd_bank_shibor.set_index('mfd_date', inplace = True)
    mfd_bank_shibor = mfd_bank_shibor.resample('D', fill_method = 'bfill')
    return mfd_bank_shibor
 
# example to support global datamember
# x = 0
# def get_x():
#     global x
#     print (x)
#     if (x == 0):
#         x = 1
#     print (x)
# 
# get_x()