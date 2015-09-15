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
import rWrapper
r_ARIMA_predict = rWrapper.r_ARIMA_predict
r_GARCH_predict = rWrapper.r_GARCH_predict

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
# AcfPacfPlot(Interest_O_N, 'Interest_O_N_')
# 
# Interest_O_N_delta1 = delta1(Interest_O_N)
# Interest_O_N_delta1.plot()
# AcfPacfPlot(Interest_O_N_delta1, 'Interest_O_N_delta1_')

start_time = datetime(2013, 7, 1)
split_time = datetime(2014, 8, 1)

Interest_O_N_X = Interest_O_N[start_time : (split_time - Day())]
Interest_O_N_y = Interest_O_N[split_time : ]
Interest_0_N_predict_loacal, Interest_0_N_residuals_local = r_ARIMA_predict(Interest_O_N_X, 
                                                    fromDate = '2014-08-01', toDate = '2014-08-31',
                                                    order = [1, 1, 8])
# Interest_0_N_predict_local.plot()

Interest_0_N_predict_online, Interest_0_N_residuals_online = r_ARIMA_predict(Interest_O_N, 
                                                    fromDate = '2014-09-01', toDate = '2014-09-30',
                                                    order = [1, 1, 8])
Interest_0_N_predict_online.plot()



# Interest_1_W
Interest_1_W = mfd_bank_shibor['Interest_1_W']
# Interest_1_W.plot()
# AcfPacfPlot(Interest_1_W, 'Interest_1_W_')
# 
# Interest_1_W_delta1 = delta1(Interest_1_W)
# Interest_1_W_delta1.plot()
# AcfPacfPlot(Interest_1_W_delta1, 'Interest_1_W_delta1')

Interest_1_W_X = Interest_1_W[start_time : (split_time - Day())]
Interest_1_W_y = Interest_1_W[split_time : ]
Interest_1_W_predict_local, Interest_1_W_residuals_local = r_ARIMA_predict(Interest_1_W_X, 
                                                    fromDate = '2014-08-01', toDate = '2014-08-31',
                                                    order = [9, 1, 9])
# Interest_1_W_predict.plot()
Interest_1_W_predict_online, Interest_1_W_residuals_online = r_ARIMA_predict(Interest_1_W, 
                                                    fromDate = '2014-09-01', toDate = '2014-09-30',
                                                    order = [9, 1, 9])
Interest_1_W_predict_online.plot()


# Interest_2_W
Interest_2_W = mfd_bank_shibor['Interest_2_W']
# Interest_2_W.plot()
# AcfPacfPlot(Interest_2_W, 'Interest_2_W_')
# 
# Interest_2_W_delta1 = delta1(Interest_2_W)
# Interest_2_W_delta1.plot()
# AcfPacfPlot(Interest_2_W_delta1, 'Interest_2_W_delta1')

Interest_2_W_X = Interest_2_W[start_time : (split_time - Day())]
Interest_2_W_y = Interest_2_W[split_time : ]
Interest_2_W_predict_local, Interest_2_W_residuals_local = r_ARIMA_predict(Interest_2_W_X, 
                                                    fromDate = '2014-08-01', toDate = '2014-08-31',
                                                    order = [2, 1, 7])                                               
Interest_2_W_predict_local.plot()
Interest_2_W_predict_online, Interest_2_W_residuals_online = r_ARIMA_predict(Interest_2_W_X, 
                                                    fromDate = '2014-09-01', toDate = '2014-09-30',
                                                    order = [2, 1, 7])  
Interest_2_W_predict_online.plot()     

# Interest_6_M
Interest_6_M = mfd_bank_shibor['Interest_6_M']
Interest_6_M.plot()
AcfPacfPlot(Interest_6_M, 'Interest_6_M_')

Interest_6_M_delta1 = delta1(Interest_6_M)
Interest_6_M_delta1.plot()
AcfPacfPlot(Interest_6_M_delta1, 'Interest_6_M_delta1')

Interest_6_M_X = Interest_6_M[start_time : (split_time - Day())]
Interest_6_M_y = Interest_6_M[split_time : ]
Interest_6_M_predict_local, Interest_6_M_residuals_local = r_ARIMA_predict(Interest_6_M_X, 
                                                    fromDate = '2014-08-01', toDate = '2014-08-31',
                                                    order = [9, 1, 18])                                               
Interest_6_M_predict_local.plot()
Interest_6_M_predict_online, Interest_6_M_residuals_online = r_ARIMA_predict(Interest_6_M_X, 
                                                    fromDate = '2014-09-01', toDate = '2014-09-30',
                                                    order = [9, 1, 18])  
Interest_6_M_predict_online.plot()   
Interest_6_M_total = pd.concat([Interest_6_M, Interest_6_M_predict_online])

# Interest_9_M
Interest_9_M = mfd_bank_shibor['Interest_9_M']
Interest_9_M.plot()
AcfPacfPlot(Interest_9_M, 'Interest_9_M_')

Interest_9_M_delta1 = delta1(Interest_9_M)
Interest_9_M_delta1.plot()
AcfPacfPlot(Interest_9_M_delta1, 'Interest_9_M_delta1')

Interest_9_M_X = Interest_9_M[start_time : (split_time - Day())]
Interest_9_M_y = Interest_9_M[split_time : ]
Interest_9_M_predict_local, Interest_9_M_residuals_local = r_ARIMA_predict(Interest_9_M_X, 
                                                    fromDate = '2014-08-01', toDate = '2014-08-31',
                                                    order = [3, 1, 13])                                               
Interest_9_M_predict_local.plot()
Interest_9_M_predict_online, Interest_9_M_residuals_online = r_ARIMA_predict(Interest_9_M_X, 
                                                    fromDate = '2014-09-01', toDate = '2014-09-30',
                                                    order = [3, 1, 13])  
Interest_9_M_predict_online.plot() 
Interest_9_M_total = pd.concat([Interest_9_M, Interest_9_M_predict_online])

# Interest_1_Y
Interest_1_Y = mfd_bank_shibor['Interest_1_Y']
Interest_1_Y.plot()
AcfPacfPlot(Interest_1_Y, 'Interest_1_Y_')

Interest_1_Y_delta1 = delta1(Interest_1_Y)
Interest_1_Y_delta1.plot()
AcfPacfPlot(Interest_1_Y_delta1, 'Interest_1_Y_delta1')

Interest_1_Y_X = Interest_1_Y[start_time : (split_time - Day())]
Interest_1_Y_y = Interest_1_Y[split_time : ]
Interest_1_Y_predict_local, Interest_1_Y_residuals_local = r_ARIMA_predict(Interest_1_Y_X, 
                                                    fromDate = '2014-08-01', toDate = '2014-08-31',
                                                    order = [3, 1, 15])                                               
Interest_1_Y_predict_local.plot()
Interest_1_Y_predict_online, Interest_1_Y_residuals_online = r_ARIMA_predict(Interest_1_Y_X, 
                                                    fromDate = '2014-09-01', toDate = '2014-09-30',
                                                    order = [3, 1, 13])  
Interest_1_Y_predict_online.plot()  

Interest_1_Y_total = pd.concat([Interest_1_Y, Interest_1_Y_predict_online])

############### concat all
Interest_total = pd.concat([Interest_6_M_total, Interest_9_M_total, Interest_1_Y_total], axis = 1)
Interest_total.to_csv('z:\\theblueisland\\raw_data\\Interest_total.csv')