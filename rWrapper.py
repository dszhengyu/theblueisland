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
trainFileARIMA = rDir + 'trainFileARIMA.csv'
predictFileARIMA = rDir + 'predictFileARIMA.csv'
residualsFileARIMA = rDir + 'residualsFileARIMA.csv'
rFileARIMA = rDir + 'arimaPredict.R'

trainFileGARCH = rDir + 'trainFileGARCH.csv'
predictFileGARCH = rDir + 'predictFileGARCH.csv'
residualsFileGARCH = rDir + 'residualsFileGARCH.csv'
rFileGARCH = rDir + 'garchPredict.R'

trainFileANN = rDir + 'trainFileANN.csv'
predictFileANN = rDir + 'predictFileANN.csv'
residualsFileANN = rDir + 'residualsFileANN.csv'
rFileANN = rDir + 'annPredict.R'

def r_ARIMA_predict(train, fromDate, toDate, order = [0, 0, 0], auto = 0):
    # use file to communicate first
    train.to_csv(trainFileARIMA, index = None)
    print ('order = ', order)
    #print ('fromDate: ', fromDate)
    #print ('toDate: ', toDate)
    
    # mixup parameter
    t = datetime.strptime(toDate, "%Y-%m-%d")
    f = datetime.strptime(fromDate, "%Y-%m-%d")
    predictDays = (t - f).days + 1
    predictDaysLine = 'predictDays = %s\n' % (predictDays)
    orderParameterLine = 'orderUsed = c(%s, %s, %s)\n' % (order[0], order[1], order[2])
    autoParameterLine = 'auto = %s\n' % (auto)
    parametersLine = orderParameterLine + predictDaysLine + autoParameterLine
    
    # manipulate in R
    rScript = open(rFileARIMA).read()
    rScript = parametersLine + rScript
    #print (rScript)
    robjects.r(rScript)
    
    predict = pd.read_csv(predictFileARIMA)
    predict = predict['x']
    predict.index = pd.date_range(fromDate, toDate)
    
    residuals = pd.read_csv(residualsFileARIMA)
    
    return (predict, residuals)
    
def r_GARCH_predict(train, fromDate, toDate, order = [20, 3]):
    # use file to communicate first
    train.to_csv(trainFileGARCH, index = None)
    print ('order = ', order)
    #print ('fromDate: ', fromDate)
    #print ('toDate: ', toDate)
    
    # mixup parameter
    t = datetime.strptime(toDate, "%Y-%m-%d")
    f = datetime.strptime(fromDate, "%Y-%m-%d")
    predictDays = (t - f).days + 1
    predictDaysLine = 'predictDays = %s\n' % (predictDays)
    orderParameterLine = 'arma = c(%s, %s)\n' % (order[0], order[1])
    parametersLine = predictDaysLine + orderParameterLine
    
    # manipulate in R
    rScript = open(rFileGARCH).read()
    rScript = parametersLine + rScript
    #print (rScript)
    robjects.r(rScript)
    
    predict = pd.read_csv(predictFileGARCH, header = None, skiprows = [0])
    predict = predict[0]
    predict.index = pd.date_range(fromDate, toDate)
    residuals = pd.read_csv(residualsFileGARCH)
    
    return (predict, residuals)
    

def r_ANN_local(beginDate):
    # save timeVector into file
    
    # write online = 0 into R script
    
    # run R script
    
    # read mean_squared_error and errorVar from file
    
    # print mean_squared_error
    
    return errorVar
        
def r_ANN_online():
    # save timeVector into file
    
    #write online = 1 into R script

    # run R script
    
    # read predict from file
    
    return predict
    
    