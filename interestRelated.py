from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas.tseries.offsets import Day
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from scipy.stats import normaltest
import statsmodels as sm
from statsmodels.tsa.arima_model import ARIMA, ARMA
from statsmodels.tsa.stattools import acf, pacf, arma_order_select_ic

from dataFactory import get_user_balance, get_day_share_interest, get_mfd_bank_shibor
from easyRude import AcfPacfPlot, delta1

user_balance = get_user_balance()
timeGroup = user_balance.groupby(['report_date'])
purchaseRedeemTotal = timeGroup['total_purchase_amt', 'total_redeem_amt'].sum()

day_share_interest = get_day_share_interest()
mfd_bank_shibor = get_mfd_bank_shibor()

all = pd.concat([purchaseRedeemTotal, day_share_interest, mfd_bank_shibor], axis = 1)
corr = all.corr()[['total_purchase_amt', 'total_redeem_amt']]


## plot & analyse
# Interest_O_N
Interest_O_N = mfd_bank_shibor['Interest_O_N']
Interest_O_N.plot()
AcfPacfPlot(Interest_O_N, 'Interest_O_N_')

Interest_O_N_delta1 = delta1(Interest_O_N)
Interest_O_N_delta1.plot()
AcfPacfPlot(Interest_O_N_delta1, 'Interest_O_N_delta1_')
Interest_O_N_delta1_predict = ARIMA(Interest_O_N_delta1, [8, 1, 8]).fit(trend='nc').predict()
Interest_O_N_delta1_predict.plot()

start_time = datetime(2013, 7, 1)
split_time = datetime(2014, 8, 1)

Interest_O_N_X = Interest_O_N[start_time : (split_time - Day())]
Interest_O_N_y = Interest_O_N[split_time : ]
Interest_O_N_model = ARIMA(Interest_O_N_X, [8, 1, 8]).fit(trend = 'nc')
Interest_O_N_predict = Interest_O_N_model.predict('2014-08-01', '2014-08-31', typ = 'levels')
Interest_O_N_predict.plot()

# Interest_1_W
Interest_1_W = mfd_bank_shibor['Interest_1_W']
Interest_1_W.plot()
AcfPacfPlot(Interest_1_W, 'Interest_1_W_')

Interest_1_W_delta1 = delta1(Interest_1_W)
Interest_1_W_delta1.plot()
AcfPacfPlot(Interest_1_W_delta1, 'Interest_1_W_delta1')
Interest_1_W_delta1_predict = ARIMA(Interest_1_W_delta1, [2, 0, 2]).fit().predict()
Interest_1_W_delta1_predict.plot()

Interest_1_W_X = Interest_1_W[start_time : (split_time - Day())]
Interest_1_W_y = Interest_1_W[split_time : ]
Interest_1_W_model = ARIMA(Interest_1_W_X, [2, 1, 2]).fit(trend='nc')
Interest_1_W_predict = Interest_1_W_model.predict('2014-08-01', '2014-08-31', typ = 'levels')
Interest_1_W_predict.plot()




Interest_2_W = mfd_bank_shibor['Interest_2_W']
Interest_2_W.plot()