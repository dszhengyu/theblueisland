# 好像不会是重点, 因为越到后面增幅约小影响越小
# 代码很乱, 主要是因为之前用statsmodels结果有一些地方很奇怪==
# 先放着吧
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas.tseries.offsets import Day
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import statsmodels as sm
from statsmodels.tsa.arima_model import ARIMA, ARMA

from easyRude import AcfPacfPlot
from dataFactory import get_user_balance, get_user_balance_clean
from rWrapper import r_ARIMA_predict

# purchase new commer
def purchaseNewUserModel(purchaseSet, online = 0, debug = 0):
    result = pd.Series(index = range(1, 31))
    for i in range(1, 31):
        print ("!!!!!!!!!!!!!!!!!!!!!", i)
        if (debug == 1):
            purchaseVirginTotal = purchaseSet.ix[i, 'total_purchase_amt']
            purchaseVirginTotal.plot(label = 'actual', legend = True)
        purchaseVirginX = purchaseSet.ix[i, 'total_purchase_amt']
        if (i != 1):
            purchaseVirginX = purchaseVirginX.resample('M', fill_method = 'ffill', label = 'left', 
                                                        loffset = '1d')
        purchaseVirginYPredict, _ = r_ARIMA_predict(purchaseVirginX, '2014-08-1', '2014-08-1', auto = 1)
        purchaseVirginYPredict.index = purchaseVirginYPredict.index + (i - 1) * Day()
        if (debug == 1):
            purchaseVirginYPredict.plot(label = 'predict', legend = True, style = 'o')
        result[i] = purchaseVirginYPredict
    if (online == 0):
        result.index = pd.date_range('2014-08-01', '2014-08-30')
    else:
        result.index = pd.date_range('2014-09-01', '2014-09-30')
    return result
    
    # #model debug
    # i = 21
    # purchaseVirginTotal = purchaseRedeemVirgin.ix[i, 'total_purchase_amt']
    # purchaseVirginTotal.plot(label = 'actual', legend = True)
    # purchaseVirginX = purchaseRedeemVirginX.ix[i, 'total_purchase_amt']
    # X = purchaseVirginX.resample('M', fill_method = 'ffill', label = 'left', loffset = '1d')
    # predict = ARIMA(X, [3, 0, 0]).fit().predict('2014-08-1', '2014-08-2', dynamic=True)
    # predict.index = predict.index + (i - 1) * Day()
    # predict.plot(style = 'o')
    # actual = purchaseRedeemVirginy.ix[i, 'total_purchase_amt']
    # print (str(i) + 'th day, mean squared error = ', mean_squared_error(actual, predict))
    
def redeemNewUserModel(redeemSet, online = 0, debug = 0):
    result = pd.Series(index = range(1, 31))
    for i in range(1, 31):
        print ("!!!!!!!!!!!!!!!!!!!!!", i)
        if (debug == 1):
            redeemVirginTotal = redeemSet.ix[i, 'total_redeem_amt']
            redeemVirginTotal.plot(label = 'actual', legend = True)
        redeemVirginX = redeemSet.ix[i, 'total_redeem_amt']
        if (i != 1):
            redeemVirginX =redeemVirginX.resample('M', fill_method = 'ffill', label = 'left', 
                                                        loffset = '1d')
        redeemVirginYPredict, _ = r_ARIMA_predict(redeemVirginX, '2014-08-1', '2014-08-1', auto = 1)
        redeemVirginYPredict.index = redeemVirginYPredict.index + (i - 1) * Day()
        result[i] = redeemVirginYPredict
        if (debug == 1):
            redeemVirginYPredict.plot(label = 'predict', legend = True, style = 'o')
    if (online == 0):
        result.index = pd.date_range('2014-08-01', '2014-08-30')
    else:
        result.index = pd.date_range('2014-09-01', '2014-09-30')
    return result
    
def newUserPredict(fromDate = '2014-01-01', online = 0):
    user_balance = get_user_balance()
    #user_balance_clean = get_user_balance_clean()
    user_balance = user_balance[user_balance['report_date'] >= fromDate]
    userGroup = user_balance.groupby('user_id')
    userVirginDay = DataFrame(userGroup['report_date'].min())
    userVirginDay.columns = ['virgin_date']
    user_balance_virginDay = pd.merge(user_balance, userVirginDay, 
                                        left_on = ['user_id'], right_index = True)
    user_balance_virginDay['virginDayinMonth'] = user_balance_virginDay['virgin_date'].map(lambda date : date.day)
    virginDayGroup = user_balance_virginDay.groupby('virgin_date')
    purchaseRedeemVirgin = virginDayGroup.agg({'total_purchase_amt' : 'sum', 
                                                'total_redeem_amt' : 'sum', 'virginDayinMonth' : 'min'})
    purchaseRedeemVirgin.reset_index(inplace = True)
    # remove first month
    purchaseRedeemVirgin = purchaseRedeemVirgin[purchaseRedeemVirgin['virgin_date'] > datetime(2013, 7, 31)]
    #validationCorrectness = virginDayGroup['user_id'].nunique().resample('M', how = 'sum', kind = 'period')
    
    # split
    split_time = datetime.strptime('20140801', "%Y%m%d")
    purchaseRedeemVirginX = purchaseRedeemVirgin[purchaseRedeemVirgin['virgin_date'] < split_time]
    purchaseRedeemVirginX.set_index(['virginDayinMonth', 'virgin_date'], inplace = True)
    purchaseRedeemVirginX = purchaseRedeemVirginX.sort_index()
    purchaseRedeemVirginy = purchaseRedeemVirgin[purchaseRedeemVirgin['virgin_date'] >= split_time]
    purchaseRedeemVirginy.set_index(['virginDayinMonth', 'virgin_date'], inplace = True)
    purchaseRedeemVirginy = purchaseRedeemVirginy.sort_index()
    purchaseRedeemVirgin.set_index(['virginDayinMonth', 'virgin_date'], inplace = True)
    purchaseRedeemVirgin = purchaseRedeemVirgin.sort_index()
    # AcfPacfPlot(purchaseRedeemVirgin, 'purchaseRedeemVirgin')
    
    purchaseNewPredict = 0
    redeemNewPredict = 0
    if (online == 0):
        purchaseNewUserModel(purchaseRedeemVirginX, debug = 1)              
        redeemNewUserModel(purchaseRedeemVirginX, debug = 1)
    else:
        purchaseNewPredict = purchaseNewUserModel(purchaseRedeemVirgin, online = 1)
        redeemNewPredict = redeemNewUserModel(purchaseRedeemVirgin, online = 1)
        
    return (purchaseNewPredict, redeemNewPredict)
        
if __name__ == '__main__': newUserPredict()