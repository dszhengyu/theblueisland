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

fromDate = '2014-08-01'
toDate = '2014-08-31'
beginDate = '2014-03-01'
online = 0
debug = 0

def delta1(origin):
    delta1 = pd.Series(index = origin.index)
    delta1 = delta1[1 : ]
    for i in range(0, delta1.size):
        delta1[i] = origin[i + 1] - origin[i]
    return delta1
    
def AcfPacfPlot(set, title):
    plt.figure()
    DataFrame(acf(set)).plot(title = title + 'ACF', kind = 'bar')
    DataFrame(pacf(set)).plot(title = title + 'PACF', kind = 'bar')
   
def analyseARIMA():
    beginDate = '2014-02-01'
    from dataFactory import get_user_balance, get_user_balance_clean
    pwd = 'z:\\theblueisland\\'
    user_balance = get_user_balance()
    user_balance = user_balance[user_balance['report_date'] >= beginDate]
    user_balance_clean = get_user_balance_clean()
    user_balance_clean = user_balance_clean[user_balance_clean['report_date'] >= beginDate]
    user_balance_clean.plot()
    # sum data
    timeGroup = user_balance_clean.groupby(['report_date'])
    purchaseRedeemTotal = timeGroup['total_purchase_amt', 'total_redeem_amt'].sum()

    # analyse acf, pacf
    AcfPacfPlot(purchaseRedeemTotal['total_purchase_amt'], 'purchase')
    AcfPacfPlot(purchaseRedeemTotal['total_redeem_amt'], 'redeem')
    
    # delta 1, purchase
    p = purchaseRedeemTotal['total_purchase_amt']
    pDelta1 = delta1(p)
    p.plot()
    pDelta1.plot() 
    AcfPacfPlot(pDelta1, 'purchaseDelta1')
    
    # delta 1, redeem
    r = purchaseRedeemTotal['total_redeem_amt']
    rDelta1 = delta1(r)
    r.plot()
    rDelta1.plot()
    AcfPacfPlot(rDelta1, 'redeemDelta1')

                          
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
    purchase.plot(title = beginDate + ' purchase')
    #AcfPacfPlot(purchase, 'purchase')
    if (online == 0):
        purchaseX = XPurchaseRedeemTotal['total_purchase_amt']
    else:
        purchaseX = purchaseRedeemTotal['total_purchase_amt']
    purchaseModel = ARIMA(purchaseX, [20, 0, 3]).fit() # 20, 0, 3
    purchaseModelResid = purchaseModel.resid
    #purchaseModelResid.plot(title = 'purchaseModelResid')
    print ('$$$$$$$$$$purchaseModelResid normal test: ', normaltest(purchaseModelResid))
    purchaseYPredict = purchaseModel.predict(fromDate, toDate, dynamic=True)
    purchaseYPredict.plot(title = beginDate + ' purchase', label = 'purchasePredictNoNew', 
                            legend = True)
    if (online == 0):
        purchaseYActual = yPurchaseRedeemTotal['total_purchase_amt']
        print ('beginDate = ', beginDate)
        print ("@@@@@@@@@@purchaseNoNew mean_squared_error = ", 
                mean_squared_error(purchaseYActual, purchaseYPredict))
    
    ## redeem
    redeem = purchaseRedeemTotal['total_redeem_amt']
    redeem.plot(title = beginDate + ' redeem')
    #AcfPacfPlot(redeem, 'redeem')
    if (online == 0):
        redeemX = XPurchaseRedeemTotal['total_redeem_amt']
    else:
        redeemX = purchaseRedeemTotal['total_redeem_amt']        
    #arma_order_select_ic(redeemX, max_ar = 20, max_ma = 20)
    redeemModel = ARIMA(redeemX, [20, 0, 2]).fit()
    redeemModelResid = redeemModel.resid
    #redeemModelResid.plot(title = 'redeemModelResid')
    print ('$$$$$$$$$$redeemModelResid normal test: ', normaltest(redeemModelResid))
    redeemYPredict = redeemModel.predict(fromDate, toDate)
    redeemYPredict.plot(title = beginDate + ' redeem', label = 'redeemPredictNoNew', 
                        legend = True)
    if (online == 0):
        redeemYActual = yPurchaseRedeemTotal['total_redeem_amt']
        print ('beginDate = ', beginDate)
        print ("@@@@@@@@@@redeemNoNew mean_squared_error = ", 
                mean_squared_error(redeemYActual, redeemYPredict))
    
    return (purchaseYPredict, redeemYPredict)

if __name__ == '__main__': purchaseRedeemPredict('2014-08-01', '2014-08-31')