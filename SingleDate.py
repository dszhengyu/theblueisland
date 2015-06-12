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

from dataFactory import get_user_balance, get_user_balance_clean, get_day_share_interest, get_mfd_bank_shibor
from easyRude import AcfPacfPlot, delta1
import rWrapper
r_ARIMA_predict = rWrapper.r_ARIMA_predict
r_GARCH_predict = rWrapper.r_GARCH_predict

user_balance_clean = get_user_balance_clean()
user_balance_clean = user_balance_clean[user_balance_clean['report_date'] > datetime(2014, 3, 1)]
timeGroup = user_balance_clean.groupby(['report_date'])
purchaseRedeemTotal = timeGroup['total_purchase_amt', 'total_redeem_amt'].sum()
purchaseRedeemTotal.reset_index(inplace = True)
purchaseRedeemTotal['dayInWeek'] = purchaseRedeemTotal['report_date'].map(lambda date: date.weekday() + 1)
purchaseRedeemTotal['dayInMonth'] = purchaseRedeemTotal['report_date'].map(lambda date: date.day)
purchaseRedeemTotal.set_index(['report_date'], inplace = True)

def testLocalDayInWeek(wholeSet, dayInWeek, order):
    # wholeSet = purchaseSaturday
    # dayInWeek = 6
    # order = [14, 1, 14]
    
    train = wholeSet[wholeSet.index < datetime(2014, 8, 1)]
    test = wholeSet[wholeSet.index >= datetime(2014, 8, 1)]
    predict, residuals = predictDayInWeek(train, dayInWeek, '20140801', '20140831', order)
    print ("day in week is ", dayInWeek)
    print ('$$$$$$$$$$ residuals normal test: ', normaltest(residuals))
    print ("@@@@@@@@@@ mean_squared_error = ", '\n', mean_squared_error(test, predict))
    errorVar = (np.abs(test - predict) / test).var()
    print ("@@@@@@@@@@ error_var = ", errorVar)
    print ()
    wholeSet.plot()
    predict.plot()
    return predict
    
    
def predictDayInWeek(train, dayInWeek, fromDate, toDate, order):
    # train = purchaseSaturday
    # fromDate = '20140901'
    # toDate = '20140930'
    # dayInWeek = 6
    # order = [14, 1, 14]
    
    # t = datetime.strptime(toDate, "%Y-%m-%d")
    # f = datetime.strptime(fromDate, "%Y-%m-%d")
    target = DataFrame(pd.date_range(fromDate, toDate))
    target = target[target[0].map(lambda date: date.weekday() == (dayInWeek - 1))]
    target.set_index([0], inplace = True)
    end = '2014-09-%s' % (target.index.size)
    predict, residuals = r_ARIMA_predict(train, '2014-09-01', end, order)
    predict.index = target.index
    return predict, residuals

## saturday
purchaseRedeemSaturday = purchaseRedeemTotal[purchaseRedeemTotal['dayInWeek'] == 6]
purchaseRedeemSaturday = purchaseRedeemSaturday[['total_purchase_amt', 'total_redeem_amt']]
purchaseRedeemSaturday.plot()
# purchase
purchaseSaturday = purchaseRedeemSaturday['total_purchase_amt']

# purchaseSaturday.plot()
# AcfPacfPlot(purchaseSaturday, 'purchaseSaturday')
# purchaseSaturdayDelta1 = delta1(purchaseSaturday)
# AcfPacfPlot(purchaseSaturdayDelta1, 'purchaseSaturdayDelta1')

purchaseSaturdayOrder = [0, 0, 4]
localPurchaseSaturday = testLocalDayInWeek(purchaseSaturday, 6, purchaseSaturdayOrder)
localPurchaseSaturday.name = 'purchasePredict'
purchaseSaturdayPredict, purchaseSaturdayResiduals = predictDayInWeek(purchaseSaturday, 6, 
                                                                        '2014-09-01', '2014-09-30', 
                                                                        order = purchaseSaturdayOrder)
purchaseSaturdayPredict.name = 'purchasePredict'
                                                                  
#purchaseSaturdayPredict.plot()
pd.concat([purchaseSaturday, purchaseSaturdayPredict]).plot()

# redeem
redeemSaturday = purchaseRedeemSaturday['total_redeem_amt']

# redeemSaturday.plot()
# AcfPacfPlot(redeemSaturday, 'redeemSaturday')
# redeemSaturdayDelta1 = delta1(redeemSaturday)
# AcfPacfPlot(redeemSaturdayDelta1, 'redeemSaturdayDelta1')

redeemSaturdayOrder = [0, 0, 6]
localRedeemSaturday = testLocalDayInWeek(redeemSaturday, 6, redeemSaturdayOrder)
localRedeemSaturday.name = 'redeemPredict'
redeemSaturdayPredict, redeemSaturdayResiduals = predictDayInWeek(redeemSaturday, 6, 
                                                                        '2014-09-01', '2014-09-30', 
                                                                        order = redeemSaturdayOrder)
redeemSaturdayPredict.name = 'redeemPredict'                                                                   
pd.concat([redeemSaturday, redeemSaturdayPredict]).plot()

localSaturday = pd.concat([localPurchaseSaturday, localRedeemSaturday], axis = 1)
localSaturday.index.name = 'report_date'
onlineSaturday = pd.concat([purchaseSaturdayPredict, redeemSaturdayPredict], axis = 1)
onlineSaturday.index.name = 'report_date'

## sunday
purchaseRedeemSunday = purchaseRedeemTotal[purchaseRedeemTotal['dayInWeek'] == 7]
purchaseRedeemSunday = purchaseRedeemSunday[['total_purchase_amt', 'total_redeem_amt']]
purchaseRedeemSunday.plot()
# purchase
purchaseSunday = purchaseRedeemSunday['total_purchase_amt']

purchaseSunday.plot()
AcfPacfPlot(purchaseSunday, 'purchaseSunday')
purchaseSundayDelta1 = delta1(purchaseSunday)
AcfPacfPlot(purchaseSundayDelta1, 'purchaseSundayDelta1')

purchaseSundayOrder = [2, 1, 4]
localPurchaseSunday = testLocalDayInWeek(purchaseSunday, 7, purchaseSundayOrder)
localPurchaseSunday.name = 'purchasePredict'
purchaseSundayPredict, purchaseSundayResiduals = predictDayInWeek(purchaseSunday, 7, 
                                                                '2014-09-01', '2014-09-30', 
                                                                order = purchaseSundayOrder)
purchaseSundayPredict.name = 'purchasePredict'
                                                                  
#purchaseSundayPredict.plot()
pd.concat([purchaseSunday, purchaseSundayPredict]).plot()

# redeem
redeemSunday = purchaseRedeemSunday['total_redeem_amt']

redeemSunday.plot()
AcfPacfPlot(redeemSunday, 'redeemSunday')
redeemSundayDelta1 = delta1(redeemSunday)
AcfPacfPlot(redeemSundayDelta1, 'redeemSundayDelta1')

redeemSundayOrder = [0, 1, 4]
localRedeemSunday = testLocalDayInWeek(redeemSunday, 7, redeemSundayOrder)
localRedeemSunday.name = 'redeemPredict'
redeemSundayPredict, redeemSundayResiduals = predictDayInWeek(redeemSunday, 7, 
                                                            '2014-09-01', '2014-09-30', 
                                                            order = redeemSundayOrder)
redeemSundayPredict.name = 'redeemPredict'                                                                   
pd.concat([redeemSunday, redeemSundayPredict]).plot()

localSunday = pd.concat([localPurchaseSunday, localRedeemSunday], axis = 1)
localSunday.index.name = 'report_date'
onlineSunday = pd.concat([purchaseSundayPredict, redeemSundayPredict], axis = 1)
onlineSunday.index.name = 'report_date'

## merge all
localDayInWeek = pd.concat([localSaturday, localSunday])
localDayInWeek.to_csv('z:\\theblueisland\\raw_data\\localDayInWeek.csv')
onlineDayInWeek = pd.concat([onlineSaturday, onlineSunday])
onlineDayInWeek.to_csv('z:\\theblueisland\\raw_data\\onlineDayInWeek.csv')
