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

# from dataFactory import get_user_balance, get_user_balance_clean
import rWrapper
r_ARIMA_predict = rWrapper.r_ARIMA_predict
r_GARCH_predict = rWrapper.r_GARCH_predict
from importlib import reload
reload(rWrapper)

fromDate = '2014-08-01'
toDate = '2014-08-31'
beginDate = '2013-07-01'
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

def getPurchaseRedeemTotal():
    # user_balance = get_user_balance()
    # user_balance = user_balance[user_balance['report_date'] >= beginDate]
    # user_balance_clean = get_user_balance_clean()
    # user_balance_clean = user_balance_clean[user_balance_clean['report_date'] >= beginDate]
    # user_balance_clean.plot()
    # # sum data
    # timeGroup = user_balance_clean.groupby(['report_date'])
    # purchaseRedeemTotal = timeGroup['total_purchase_amt', 'total_redeem_amt'].sum()
    
    # use the season2 data
    purchaseRedeemTotal = pd.read_csv('z:\\theblueisland\\Season2\\daily_purchase_redeem.csv',
                            parse_dates = ['report_date'], index_col = ['report_date'])
    purchaseRedeemTotal.columns= ['total_purchase_amt', 'total_redeem_amt']
    return purchaseRedeemTotal
   
def analyseARIMA():
    beginDate = '2014-02-01'
    purchaseRedeemTotal = getPurchaseRedeemTotal()

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

def purchaseRedeemTotalFactory(beginDate = '2013-11-01'):
    
    purchaseRedeemTotal = getPurchaseRedeemTotal()
    
    # split X y
    start_time = datetime.strptime(beginDate, "%Y-%m-%d")
    split_time = datetime.strptime('20140801', "%Y%m%d")
    
    # user_balance_X = user_balance_clean[user_balance_clean['report_date'] < split_time]
    # XTimeGroup = user_balance_X.groupby(['report_date'])
    # XPurchaseRedeemTotal = XTimeGroup['total_purchase_amt', 'total_redeem_amt'].sum()
    # 
    # user_balance_y = user_balance_clean[user_balance_clean['report_date'] >= split_time]
    # yTimeGroup = user_balance_y.groupby(['report_date'])
    # yPurchaseRedeemTotal = yTimeGroup['total_purchase_amt', 'total_redeem_amt'].sum()
    
    purchaseRedeemTotal = purchaseRedeemTotal.ix[start_time : ]
    XPurchaseRedeemTotal = purchaseRedeemTotal.ix[start_time : split_time - Day()]
    yPurchaseRedeemTotal = purchaseRedeemTotal.ix[split_time : ]
    
    return (purchaseRedeemTotal, XPurchaseRedeemTotal, yPurchaseRedeemTotal)
                          
def purchaseRedeemPredict(fromDate = '2014-08-01', toDate = '2014-08-31',
                          beginDate = '2014-04-01', online = 0, debug = 0, 
                          order = (([2, 1, 2], [1, 1, 0]), ([2, 1, 1], [1, 1, 0]))):
                              
    # get purchaseRedeemTotalResult
    purchaseRedeemTotalResult = purchaseRedeemTotalFactory(beginDate = beginDate)
    purchaseRedeemTotal = purchaseRedeemTotalResult[0]
    XPurchaseRedeemTotal = purchaseRedeemTotalResult[1] 
    yPurchaseRedeemTotal = purchaseRedeemTotalResult[2] 
    
    ## purchase
    plt.figure()
    purchase = purchaseRedeemTotal['total_purchase_amt']
    purchase.plot(title = beginDate + ' purchase')
    # # analyse bellow
    # AcfPacfPlot(purchase, 'purchase')
    # purchaseDelta1 = delta1(purchase)
    # purchaseDelta1.plot(title = beginDate + ' purchaseDelta1')
    # AcfPacfPlot(purchaseDelta1, 'purchaseDelta1')
    
    # purchaseDelta2 = delta1(purchaseDelta1)
    # purchaseDelta2.plot(title = beginDate + ' purchaseDelta2')
    # AcfPacfPlot(purchaseDelta2, 'purchaseDelta2')
    
    # purchaseDelta3 = delta1(purchaseDelta2)
    # purchaseDelta3.plot(title = beginDate + ' purchaseDelta3')
    # AcfPacfPlot(purchaseDelta3, 'purchaseDelta3')
    
    if (online == 0):
        purchaseX = XPurchaseRedeemTotal['total_purchase_amt']
    else:
        purchaseX = purchaseRedeemTotal['total_purchase_amt']
        
 
    purchaseYPredict, purchaseModelResid = r_ARIMA_predict(purchaseX, fromDate, toDate, 
                                                        orderTotal = order[0], auto = 0)
    # purchaseYPredict, purchaseModelResid = r_ARIMA_predict(purchaseX, fromDate, toDate,  
    # orderTotal = ([0, 1, 2], [1, 1, 0]), auto = 0)
    purchaseYPredict.plot(title = beginDate + ' purchase', label = 'purchasePredictNoNew', legend = True)
    print ('$$$$$$$$$$purchaseModelResid normal test: ', normaltest(purchaseModelResid))
    #purchaseModelResid.plot(title = 'purchaseModelResid')
    
    purchaseErrorVar = 0
    if (online == 0):
        purchaseYActual = yPurchaseRedeemTotal['total_purchase_amt']
        print ('beginDate = ', beginDate)
        print ("@@@@@@@@@@purchaseNoNew mean_squared_error = ", 
                mean_squared_error(purchaseYActual, purchaseYPredict))
        purchaseErrorVar = (np.abs(purchaseYActual - purchaseYPredict) / purchaseYActual).var()
    
    ## redeem
    redeem = purchaseRedeemTotal['total_redeem_amt']
    redeem.plot(title = beginDate + ' redeem')
    # # analyse bellow
    # AcfPacfPlot(redeem, 'redeem')
    
    # redeemLog = np.log(redeem)
    # redeemLog.plot(title = beginDate + ' redeem')
    # AcfPacfPlot(redeemLog, 'redeemLog')
    
    # redeemDelta1 = delta1(redeem)
    # redeemDelta1.plot(title = beginDate + ' redeemDelta1')
    # AcfPacfPlot(redeemDelta1, 'redeemDelta1')

    # 
    # redeemDelta2 = delta1(redeemDelta1)
    # redeemDelta2.plot(title = beginDate + ' redeemDelta1')
    # AcfPacfPlot(redeemDelta2, 'redeemDelta2')
    # redeemDelta2_predict = r_ARIMA_predict
    # redeemDelta2_predict.plot()

    if (online == 0):
        redeemX = XPurchaseRedeemTotal['total_redeem_amt']
    else:
        redeemX = purchaseRedeemTotal['total_redeem_amt']        

    # log transformation
    # redeemX = np.log(redeemX) 
    redeemYPredict, redeemModelResid = r_ARIMA_predict(redeemX, fromDate, toDate, 
                                                        orderTotal = order[1], auto = 0)
    # redeemYPredict, redeemModelResid = r_ARIMA_predict(redeemX, fromDate, toDate, 
    # orderTotal = ([2, 1, 2], [1, 1, 0]), auto = 0)
    # log back transformation
    #redeemYPredict = np.exp(redeemYPredict)
    redeemYPredict.plot(title = beginDate + ' redeem', label = 'redeemPredictNoNew', legend = True)
    #redeemModelResid.plot(title = 'redeemModelResid')
    print ('$$$$$$$$$$redeemModelResid normal test: ', normaltest(redeemModelResid))
    
    redeemErrorVar = 0
    if (online == 0):
        redeemYActual = yPurchaseRedeemTotal['total_redeem_amt']
        print ('beginDate = ', beginDate)
        print ("@@@@@@@@@@redeemNoNew mean_squared_error = ", 
                mean_squared_error(redeemYActual, redeemYPredict))
        redeemErrorVar = (np.abs(redeemYActual - redeemYPredict) / redeemYPredict).var()
    
    return (purchaseYPredict, redeemYPredict, purchaseErrorVar, redeemErrorVar)
    
    # beginDate = '2014-04-01'
def garchPurchaseRedeemPredict(fromDate = '2014-08-01', toDate = '2014-08-31',
                          beginDate = '2013-07-01', online = 0, debug = 0, 
                          order = ([20, 3], [20, 3])):
                              
    # get purchaseRedeemTotalResult
    purchaseRedeemTotalResult = purchaseRedeemTotalFactory(beginDate = beginDate)
    purchaseRedeemTotal = purchaseRedeemTotalResult[0]
    XPurchaseRedeemTotal = purchaseRedeemTotalResult[1] 
    yPurchaseRedeemTotal = purchaseRedeemTotalResult[2] 
    
    ## purchase
    plt.figure()
    purchase = purchaseRedeemTotal['total_purchase_amt']
    purchase.plot(title = beginDate + ' purchase')
    # # analyse bellow
    # AcfPacfPlot(purchase, 'purchase')
    
    if (online == 0):
        purchaseX = XPurchaseRedeemTotal['total_purchase_amt']
    else:
        purchaseX = purchaseRedeemTotal['total_purchase_amt']
        
    purchaseYPredict, purchaseModelResid = r_GARCH_predict(purchaseX, fromDate, toDate, order = order[0])
    # purchaseYPredict, purchaseModelResid = r_GARCH_predict(purchaseX, fromDate, toDate, order = [7, 11])
    purchaseYPredict.plot(title = beginDate + ' purchase', label = 'purchasePredictNoNew', legend = True)
    print ('$$$$$$$$$$purchaseModelResid normal test: ', normaltest(purchaseModelResid))
    
    purchaseErrorVar = 0
    if (online == 0):
        purchaseYActual = yPurchaseRedeemTotal['total_purchase_amt']
        print ('beginDate = ', beginDate)
        print ("@@@@@@@@@@purchaseNoNew mean_squared_error = ", 
                mean_squared_error(purchaseYActual, purchaseYPredict))
        purchaseErrorVar = (np.abs(purchaseYActual - purchaseYPredict) / purchaseYActual).var()
    
    ## redeem
    redeem = purchaseRedeemTotal['total_redeem_amt']
    redeem.plot(title = beginDate + ' redeem')
    # # analyse bellow
    # AcfPacfPlot(redeem, 'redeem')

    if (online == 0):
        redeemX = XPurchaseRedeemTotal['total_redeem_amt']
    else:
        redeemX = purchaseRedeemTotal['total_redeem_amt']        

    redeemYPredict, redeemModelResid = r_GARCH_predict(redeemX, fromDate, toDate, order = order[1])
    #redeemYPredict, redeemModelResid = r_GARCH_predict(redeemX, fromDate, toDate, order = [8, 10])
    redeemYPredict.plot(title = beginDate + ' redeem', label = 'redeemPredictNoNew', legend = True)
    print ('$$$$$$$$$$redeemModelResid normal test: ', normaltest(redeemModelResid))
    
    redeemErrorVar = 0
    if (online == 0):
        redeemYActual = yPurchaseRedeemTotal['total_redeem_amt']
        print ('beginDate = ', beginDate)
        print ("@@@@@@@@@@redeemNoNew mean_squared_error = ", 
                mean_squared_error(redeemYActual, redeemYPredict))
        redeemErrorVar = (np.abs(redeemYActual - redeemYPredict) / redeemYPredict).var()
    
    return (purchaseYPredict, redeemYPredict, purchaseErrorVar, redeemErrorVar)
    

def purchaseRedeemPredictOnlineEasy(beginDate, order, 
                                    fromDate = '2014-09-01', 
                                    toDate = '2014-09-30'):
    purchasePredict, redeemPredict,  purchaseErrorVar, redeemErrorVar = purchaseRedeemPredict(fromDate, toDate, 
                                                             beginDate, online = 1, 
                                                             debug = 0, order = order)
    return (purchasePredict, redeemPredict)

def purchaseRedeemPredictOnlineEasyGarch(beginDate, order, 
                                    fromDate = '2014-09-01', 
                                    toDate = '2014-09-30'):
    purchasePredict, redeemPredict,  purchaseErrorVar, redeemErrorVar = garchPurchaseRedeemPredict(fromDate, toDate, 
                                                             beginDate, online = 1, 
                                                             debug = 0, order = order)
    return (purchasePredict, redeemPredict)
    
def purchaseRedeemPredictLocalAndErrorVar(beginDate, order, 
                                    fromDate = '2014-08-01', 
                                    toDate = '2014-08-31'):
    purchasePredict, redeemPredict, purchaseErrorVar, redeemErrorVar = purchaseRedeemPredict(fromDate, toDate, 
                                                             beginDate, online = 0, 
                                                             debug = 0, order = order)
    return ((purchasePredict, redeemPredict), (purchaseErrorVar, redeemErrorVar))

def purchaseRedeemPredictLocalAndErrorVarGarch(beginDate, order, 
                                    fromDate = '2014-08-01', 
                                    toDate = '2014-08-31'):
    purchasePredict, redeemPredict, purchaseErrorVar, redeemErrorVar = garchPurchaseRedeemPredict(fromDate, toDate, 
                                                             beginDate, online = 0, 
                                                             debug = 0, order = order)
    return ((purchasePredict, redeemPredict), (purchaseErrorVar, redeemErrorVar))
    
    
def purchaseRedeemModelEvaluate(purchaseRedeemPredict, modelTime):
    purchaseRedeemTotal = getPurchaseRedeemTotal()
    split_time = datetime.strptime('20140801', "%Y%m%d")
    yPurchaseRedeemTotal = purchaseRedeemTotal.ix[split_time : ]
    
    purchase = purchaseRedeemTotal['total_purchase_amt']
    purchase.plot(title = 'multiModel-purchase')
    purchaseYPredict = purchaseRedeemPredict['purchasePredict']
    purchaseYPredict.plot(title = 'multiModel-purchase', label = 'purchasePredict', legend = True)
    purchaseYActual = yPurchaseRedeemTotal['total_purchase_amt']
    print ('modelTime = ', modelTime)
    print ("@@@@@@@@@@ purchase mean_squared_error = ", 
            mean_squared_error(purchaseYActual, purchaseYPredict))
    purchaseErrorVar = (np.abs(purchaseYActual - purchaseYPredict) / purchaseYActual).var()
    
    redeem = purchaseRedeemTotal['total_redeem_amt']
    redeem.plot(title = 'multiModel-redeem')
    redeemYPredict = purchaseRedeemPredict['redeemPredict']
    redeemYPredict.plot(title = 'multiModel-redeem', label = 'redeemPredict', legend = True)
    redeemYActual = yPurchaseRedeemTotal['total_redeem_amt']
    print ('modelTime = ', modelTime)
    print ("@@@@@@@@@@redeem  mean_squared_error = ", 
            mean_squared_error(redeemYActual, redeemYPredict))
    redeemErrorVar = (np.abs(redeemYActual - redeemYPredict) / redeemYPredict).var()
    
    return (purchaseErrorVar, redeemErrorVar)
    

#if __name__ == '__main__': purchaseRedeemPredict('2014-08-01', '2014-08-31')