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

from easyRude import purchaseRedeemPredict

## submit online
purchasePredict, redeemPredict = purchaseRedeemPredict(fromDate = '2014-09-01', 
                                                        toDate = '2014-09-30', online = 1,
                                                        beginDate = '2014-03-01')
                                                        
online = pd.concat([purchasePredict, redeemPredict], axis = 1)
online.to_csv(pwd + 'tc_comp_predict_table.csv', header = None, date_format = "%Y%m%d")