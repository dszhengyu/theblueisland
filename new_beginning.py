from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas.tseries.offsets import Day
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import statsmodels as sm
from statsmodels.tsa.arima_model import ARIMA, ARMA
from statsmodels.tsa.stattools import acf, pacf

from easyRude import purchaseRedeemPredictOnlineEasy
from multiDateRange import arimaMultiModelOnline



## submit online
# beginDate = '2013-07-01'
# purchasePredict, redeemPredict = purchaseRedeemPredictEasy(fromDate = '2014-09-01', 
#                                                             toDate = '2014-09-30', 
#                                                             beginDate = beginDate)
#                                                         
# online = pd.concat([purchasePredict, redeemPredict], axis = 1)

online = arimaMultiModelOnline()

online.to_csv('z:\\theblueisland\\tc_comp_predict_table.csv', header = None, date_format = "%Y%m%d")