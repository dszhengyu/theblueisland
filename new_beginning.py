from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import statsmodels as sm
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import acf, pacf

pwd = 'z:\\theblueisland\\'
featureName = pwd + 'feature.csv'
raw_data = pwd + 'raw_data\\'
user_balance_table = raw_data
user_profile_table = raw_data + 'user_profile_table.txt'
user_profile_table_parsed_date = raw_data + 'user_profile_table_parsed_date.csv'
day_share_interest_table = raw_data + 'mfd_day_share_interest.txt'
mfd_bank_shibor_table = raw_data + 'mfd_bank_shibor.txt'

## deal with slow txt
#user_balance = pd.read_csv(user_balance_table, parse_dates = ['report_date'])
#user_balance.fillna(0, inplace = True)
#user_balance.to_csv(user_profile_table_parsed_date)


## clear data
user_balance = pd.read_csv(user_profile_table_parsed_date, parse_dates = ['report_date'])
userGroup = user_balance.groupby('user_id')
pLess10 = userGroup['total_purchase_amt'].max() < 10
rLess10 = userGroup['total_redeem_amt'].max() < 10
less10 = np.logical_and(pLess10, rLess10)
toKeep = less10[less10 == False]
user_balance_clean = user_balance.set_index('user_id')
user_balance_clean = user_balance_clean.ix[toKeep.index]
user_balance_clean.reset_index(inplace = True)

## new user everyday
# could we clean data??? not clean now
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

# purchase new commer
def purchaseNewUserModel(X, fromDate, toDate):
    X.plot()
    model = ARIMA(X, [3, 0, 0]).fit()
    predict = model.predict(fromDate, toDate, dynamic=True)
    return predict

for i in range(1, 31):
    print ("!!!!!!!!!!!!!!!!!!!!!", i)
    purchaseVirginX = purchaseRedeemVirginX.ix[i, 'total_purchase_amt']
    if (i != 1):
        purchaseVirginX = purchaseVirginX.resample('M', fill_method = 'ffill', label = 'left', 
                                                    loffset = '1d')
    purchaseVirginYPredict = purchaseNewUserModel(purchaseVirginX, '2014-08-1', '2014-08-2')
    purchaseVirginYPredict.index = purchaseVirginYPredict.index + (i - 1) * Day()
    purchaseVirginYPredict.plot()
    purchaseVirginYActual = purchaseRedeemVirginy.ix[i, 'total_purchase_amt']
    purchaseVirginYActual.plot()
    print (str(i) + 'th day, mean squared error = ', mean_squared_error(purchaseVirginYActual, purchaseVirginYPredict))

    # #debug
    # i = 30
    # purchaseVirginX = purchaseRedeemVirginX.ix[i, 'total_purchase_amt']
    # X = purchaseVirginX.resample('M', fill_method = 'ffill', label = 'left', loffset = '1d')
    # fromDate = '2014-08-1'
    # toDate = '2014-08-2'
    # model = ARIMA(X, [2, 0, 0]).fit()
    # predict = model.predict(fromDate, toDate)
    # predict.index = predict.index + (i - 1) * Day()
    # predict.plot()

# purchase new commer
def redeemNewUserModel(X, fromDate, toDate):
    X.plot()
    model = ARIMA(X, [3, 0, 0]).fit()
    predict = model.predict(fromDate, toDate, dynamic=True)
    return predict

for i in range(1, 31):
    print ("!!!!!!!!!!!!!!!!!!!!!", i)
    redeemVirginX = purchaseRedeemVirginX.ix[i, 'total_redeem_amt']
    if (i != 1):
        redeemVirginX =redeemVirginX.resample('M', fill_method = 'ffill', label = 'left', 
                                                    loffset = '1d')
    redeemVirginYPredict = redeemNewUserModel(redeemVirginX, '2014-08-1', '2014-08-2')
    redeemVirginYPredict.index = redeemVirginYPredict.index + (i - 1) * Day()
    redeemVirginYPredict.plot()
    redeemVirginYActual = purchaseRedeemVirginy.ix[i, 'total_redeem_amt']
    redeemVirginYActual.plot()
    print (str(i) + 'th day, mean squared error = ', mean_squared_error(redeemVirginYActual, redeemVirginYPredict))

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
def purchaseModel(X, fromDate, toDate):
    X.plot()
    model = ARIMA(X, [10, 0, 3]).fit() # 23, 3
    predict = model.predict(fromDate, toDate, dynamic=True)
    predict.plot()
    return predict

purchaseX = XPurchaseRedeemTotal['total_purchase_amt']
purchaseYActual = yPurchaseRedeemTotal['total_purchase_amt']
purchaseYActual.plot()
purchaseYPredict = purchaseModel(purchaseX, '2014-08-01', '2014-08-31')

print ("purchase mean_squared_error = ", mean_squared_error(purchaseYActual, purchaseYPredict))

 
## redeem
def redeemModel(X, fromDate, toDate):
    X.plot()
    model = ARIMA(X, [10, 0, 2]).fit()
    predict = model.predict(fromDate, toDate, dynamic=True)
    predict.plot()
    return predict

redeemX = XPurchaseRedeemTotal['total_redeem_amt']
redeemYActual = yPurchaseRedeemTotal['total_redeem_amt']
redeemYActual.plot()
redeemYPredict = redeemModel(redeemX, '2014-08-01', '2014-08-31')
print ("redeem mean_squared_error = ", mean_squared_error(redeemYActual, redeemYPredict))

## submit online
purchaseTotal = purchaseRedeemTotal['total_purchase_amt']
purchasePredict = purchaseModel(purchaseTotal, '2014-09-01', '2014-09-30')
purchaseConcatALL = pd.concat([purchaseTotal, purchasePredict])
purchaseConcatALL.plot()

redeemTotal = purchaseRedeemTotal['total_redeem_amt']
redeemPredict = redeemModel(redeemTotal, '2014-09-01', '2014-09-30')
redeemConcatALL = pd.concat([redeemTotal, redeemPredict])
redeemConcatALL.plot()

online = pd.concat([purchasePredict, redeemPredict], axis = 1)
online.to_csv(pwd + 'tc_comp_predict_table.csv', header = None, date_format = "%Y%m%d")