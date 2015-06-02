from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas.tseries.offsets import Day
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from scipy.stats import normaltest

import rpy2.robjects as robjects

rDir = 'z:\\theblueisland\\R\\'
trainFile = rDir + 'trainFile.csv'
predictFile = rDir + 'predictFile.csv'
residualsFile = rDir + 'residualsFile.csv'
rFile = rDir + 'arimaPredict.R'

def r_ARIMA_predict(train, order, fromDate, toDate):
    # use file to communicate first
    train.to_csv(trainFile, index = None)
    print ('order = ', order)
    #print ('fromDate: ', fromDate)
    #print ('toDate: ', toDate)
    
    # mixup parameter
    t = datetime.strptime(toDate, "%Y-%m-%d")
    f = datetime.strptime(fromDate, "%Y-%m-%d")
    predictDays = (t - f).days + 1
    predictDaysLine = 'predictDays = %s\n' % (predictDays)
    orderParameterLine = 'orderUsed = c(%s, %s, %s)\n' % (order[0], order[1], order[2])
    parametersLine = orderParameterLine + predictDaysLine
    
    # manipulate in R
    rScript = open(rFile).read()
    rScript = parametersLine + rScript
    #print (rScript)
    robjects.r(rScript)
    
    predict = pd.read_csv(predictFile)
    predict = predict['x']
    predict.index = pd.date_range(fromDate, toDate)
    
    residuals = pd.read_csv(residualsFile)
    
    return (predict, residuals)
    

