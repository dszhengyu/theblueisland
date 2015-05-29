from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from pandas import DataFrame
from statsmodels.tsa.arima_model import ARIMA

pwd = 'z:\\theblueisland\\'
featureName = pwd + 'feature.csv'
raw_data = pwd + 'raw_data\\'
user_balance_table = raw_data
user_profile_table = raw_data + 'user_profile_table.txt'
user_profile_table_parsed_date = raw_data + 'user_profile_table_parsed_date.csv'
day_share_interest_table = raw_data + 'mfd_day_share_interest.txt'
mfd_bank_shibor_table = raw_data + 'mfd_bank_shibor.txt'

#user_balance = pd.read_csv(user_balance_table, parse_dates = ['report_date'])
#user_balance.fillna(0, inplace = True)
#user_balance.to_csv(user_profile_table_parsed_date)

user_balance = pd.read_csv(user_profile_table_parsed_date, parse_dates = ['report_date'])
timeGroup = user_balance.groupby(['report_date'])
purchaseRedeemTotal = timeGroup['total_purchase_amt', 'total_redeem_amt'].sum()
purchaseTotal = pd.DataFrame(purchaseRedeemTotal['total_purchase_amt'])
purchaseTotal.plot()

model = ARIMA(purchaseTotal, [1, 0, 1]).fit()
purchasePredict = model.predict('2014-09-01', '2014-09-30', dynamic=True)
purchasePredict.plot()


train_test_split_time = datetime.strptime('20140601', "%Y%m%d")
train_target_split_time = datetime.strptime('20140501', "%Y%m%d")
test_target_split_time = datetime.strptime('20140801', "%Y%m%d")

train_raw_index = user_balance['report_date'] < train_target_split_time
train_raw = user_balance[train_raw_index]
train_target_raw_index = user_balance['report_date'] >= train_target_split_time  
train_target_raw_index = train_target_raw_index & (user_balance['report_date'] < train_test_split_time)
train_target_raw = user_balance[train_target_raw_index]

test_raw_index = user_balance['report_date'] >= train_test_split_time
test_raw_index = test_raw_index & (user_balance['report_date'] < test_target_split_time)
test_raw = user_balance[test_raw_index]
test_target_raw_index = user_balance['report_date'] >= test_target_split_time  
test_target_raw = user_balance[test_target_raw_index]