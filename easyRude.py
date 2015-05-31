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

fromDate = '2014-08-01'
toDate = '2014-08-31'
beginDate = '2013-07-01'
online = 0
debug = 0

def analyseARIMA():
    beginDate = '2014-03-01'
    from dataFactory import get_user_balance, get_user_balance_clean
    pwd = 'z:\\theblueisland\\'
    user_balance = get_user_balance()
    user_balance = user_balance[user_balance['report_date'] >= beginDate]
    user_balance_clean = get_user_balance_clean()
    user_balance_clean = user_balance_clean[user_balance_clean['report_date'] >= beginDate]
    
    # sum data
    timeGroup = user_balance_clean.groupby(['report_date'])
    purchaseRedeemTotal = timeGroup['total_purchase_amt', 'total_redeem_amt'].sum()

    # analyse acf, pacf
    plt.figure()
    DataFrame(acf(purchaseRedeemTotal['total_purchase_amt'])).plot(kind = 'bar')
    DataFrame(pacf(purchaseRedeemTotal['total_purchase_amt'])).plot(kind = 'bar')
    DataFrame(acf(purchaseRedeemTotal['total_redeem_amt'])).plot(kind = 'bar')
    DataFrame(pacf(purchaseRedeemTotal['total_redeem_amt'])).plot(kind = 'bar')
    
    # delta 1, purchase
    p = purchaseRedeemTotal['total_purchase_amt']
    pDelta = pd.Series(index = p.index)
    pDelta = pDelta[1 :]
    for i in  range(0 , pDelta.size):
        pDelta[i] = p[i + 1] - p[i]
    p.plot()
    pDelta.plot()
    
    # delta 1, redeem
    r = purchaseRedeemTotal['total_redeem_amt']
    rDelta = pd.Series(index = r.index)
    rDelta = rDelta[1 : ]
    for i in  range(0 , rDelta.size):
        rDelta[i] = r[i + 1] - r[i]
    r.plot()
    rDelta.plot()

                          
def purchaseRedeemPredict(fromDate = '2014-08-01', toDate = '2014-08-31',
                          beginDate = '2013-07-01', online = 0, debug = 0):
                              
    ## get data
    from dataFactory import get_user_balance, get_user_balance_clean
    pwd = 'z:\\theblueisland\\'
    user_balance = get_user_balance()
    user_balance = user_balance[user_balance['report_date'] >= beginDate]
    user_balance_clean = get_user_balance_clean()
    user_balance_clean = user_balance_clean[user_balance_clean['report_date'] >= beginDate]
    
    ## sum purchase and redeem
    timeGroup = user_balance_clean.groupby(['report_date'])
    purchaseRedeemTotal = timeGroup['total_purchase_amt', 'total_redeem_amt'].sum()
    
    # split X y
    split_time = datetime.strptime('20140801', "%Y%m%d")
    
    user_balance_X = user_balance_clean[user_balance_clean['report_date'] < split_time]
    XTimeGroup = user_balance_X.groupby(['report_date'])
    XPurchaseRedeemTotal = XTimeGroup['total_purchase_amt', 'total_redeem_amt'].sum()
    
    user_balance_y = user_balance_clean[user_balance_clean['report_date'] >= split_time]
    yTimeGroup = user_balance_y.groupby(['report_date'])
    yPurchaseRedeemTotal = yTimeGroup['total_purchase_amt', 'total_redeem_amt'].sum()
    
    ## purchase
    plt.figure()
    purchase = purchaseRedeemTotal['total_purchase_amt']
    purchase.plot()
    if (online == 0):
        purchaseX = XPurchaseRedeemTotal['total_purchase_amt']
    else:
        purchaseX = purchaseRedeemTotal['total_purchase_amt']
    purchaseModel = ARIMA(purchaseX, [20, 0, 3]).fit() # 23, 0, 3
    purchaseYPredict = purchaseModel.predict(fromDate, toDate, dynamic=True)
    purchaseYPredict.plot(label = 'purchasePredictNoNew', legend = True)
    if (online == 0):
        purchaseYActual = yPurchaseRedeemTotal['total_purchase_amt']
        print ('beginDate = ', beginDate)
        print ("@@@@@@@@@@purchaseNoNew mean_squared_error = ", 
                mean_squared_error(purchaseYActual, purchaseYPredict))
    
    ## redeem
    plt.figure()
    redeem = purchaseRedeemTotal['total_redeem_amt']
    redeem.plot()
    if (online == 0):
        redeemX = XPurchaseRedeemTotal['total_redeem_amt']
    else:
        redeemX = purchaseRedeemTotal['total_redeem_amt']
    redeemModel = ARIMA(redeemX, [15, 0, 2]).fit()
    redeemYPredict = redeemModel.predict(fromDate, toDate, dynamic=True)
    redeemYPredict.plot(label = 'redeemPredictNoNew', legend = True)
    if (online == 0):
        redeemYActual = yPurchaseRedeemTotal['total_redeem_amt']
        print ('beginDate = ', beginDate)
        print ("@@@@@@@@@@redeemNoNew mean_squared_error = ", 
                mean_squared_error(redeemYActual, redeemYPredict))
    
    return (purchaseYPredict, redeemYPredict)

if __name__ == '__main__': purchaseRedeemPredict('2014-08-01', '2014-08-31')