from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.grid_search import GridSearchCV
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler, MinMaxScaler

pwd = 'z:\\theblueisland\\'
featureName = pwd + 'feature.csv'
raw_data = pwd + 'raw_data\\'
user_balance_table = raw_data + 'user_balance_table.txt'
user_profile_table = raw_data + 'user_profile_table.txt'
day_share_interest_table = raw_data + 'mfd_day_share_interest.txt'
mfd_bank_shibor_table = raw_data + 'mfd_bank_shibor.txt'

def extract(X, y):
    feature = extractX(X)
    
    y.loc[ : , 'dayOfMonth'] = y['report_date'].map(lambda unit: unit.day)
    yPersonDayGroup = y.groupby(['user_id', 'dayOfMonth'])
    target = yPersonDayGroup['total_purchase_amt', 'total_redeem_amt'].max()
    
    result = pd.merge(feature, target, how = 'right', left_index = True, right_index = True)
    
    #result.to_csv(featureName)
    result.fillna(0, inplace = True)
    return result
    
def extractX(X):
    X.loc[ : , 'dayOfMonth'] = X['report_date'].map(lambda unit: unit.day)
    X.loc[ : , 'dayOfWeek'] = X['report_date'].map(lambda unit: unit.weekday())
    X.loc[ : , 'month'] = X['report_date'].map(lambda unit: unit.month)
    
    personDayGroup = X.groupby(['user_id', 'dayOfMonth'])
    personDay = personDayGroup.mean()
    personDay.drop(['dayOfWeek', 'month'], axis = 1, inplace = True)
    
    personGroup = X.groupby(['user_id'])
    person = personGroup.mean()
    person.drop(['dayOfMonth', 'dayOfWeek', 'month'], axis = 1, inplace = True)
    
    feature = pd.merge(personDay, person, how = 'left', left_index = True, right_index = True)
    feature.fillna(0, inplace = True)
    return feature
    
user_balance = pd.read_csv(user_balance_table, parse_dates = ['report_date'])
user_balance.fillna(0, inplace = True)

train_test_split_time = datetime.strptime('20140601', "%Y%m%d")
train_target_split_time = datetime.strptime('20140501', "%Y%m%d")
test_target_split_time = datetime.strptime('20140801', "%Y%m%d")

train_raw_index = user_balance['report_date'] < train_target_split_time
train_raw = user_balance[train_raw_index]
train_target_raw_index = user_balance['report_date'] >= train_target_split_time  
train_target_raw_index = train_target_raw_index & (user_balance['report_date'] < train_test_split_time)
train_target_raw = user_balance[train_target_raw_index]

test_raw_index = user_balance['report_date'] >= train_test_split_time
test_raw_index = test_raw_index & (user_balance['report_date'] < test_target_split_time)
test_raw = user_balance[test_raw_index]
test_target_raw_index = user_balance['report_date'] >= test_target_split_time  
test_target_raw = user_balance[test_target_raw_index]

train = extract(train_raw, train_target_raw)
test = extract(test_raw, test_target_raw)

X_train = train.ix[ : , : -2]
X_train = MinMaxScaler().fit_transform(X_train)
y_purchase = train.ix[ : , -2]
y_redeem = train.ix[ : , -1]

X_train_test = test.ix[ : , : -2]
X_train_test = MinMaxScaler().fit_transform(X_train_test)
y_purchase_test = test.ix[ : , -2]
y_redeem_test = test.ix[ : , -1]

purchaseRegModel = Lasso()
purchaseRegModel.fit(X_train, y_purchase)
print (mean_squared_error(y_purchase, purchaseRegModel.predict(X_train)))
print ()
print (mean_squared_error(y_purchase_test, purchaseRegModel.predict(X_train_test)))
    
    