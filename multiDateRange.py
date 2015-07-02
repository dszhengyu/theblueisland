import numpy as np
import pandas as pd
from pandas import DataFrame

from easyRude import purchaseRedeemPredictLocalAndErrorVar, purchaseRedeemModelEvaluate, purchaseRedeemPredictOnlineEasy
from easyRude import purchaseRedeemPredictLocalAndErrorVarGarch, purchaseRedeemPredictOnlineEasyGarch
pwd = 'z:\\theblueisland\\'
arimaWeightFile = pwd + 'arimaWeightFile.csv'
modelTime = ['2013-11-01', '2014-03-01', '2014-04-01', '2014-05-01']
modelOrder = {'2013-11-01' : (([6, 1, 5], [1, 1, 0]), ([2, 1, 2], [1, 1, 0])),
                '2014-03-01' : (([0, 1, 2], [1, 1, 0]), ([2, 1, 2], [1, 1, 0])),
                '2014-04-01' : (([2, 1, 2], [1, 1, 0]), ([2, 1, 2], [1, 1, 0])),
                '2014-05-01' : (([2, 1, 2], [1, 1, 0]), ([2, 1, 2], [1, 1, 0]))}
                      
garchModelTime = ['2013-07-01', '2013-11-01', '2014-03-01', '2014-04-01']
garchModelOrder = {'2013-07-01' : ([20, 3], [20, 8]),
                '2013-11-01' : ([20, 3], [8, 8]),
                '2014-03-01' : ([8, 7], [7, 8]),
                '2014-04-01' : ([7, 11], [8, 10])}
                
weightArimaGarchFile = pwd + 'weightArimaGarchFile.csv'

def localMergeDayInWeek(purchaseRedeemPredict):
    localDayInWeek = pd.read_csv('z:\\theblueisland\\raw_data\\localDayInWeek.csv', 
                                index_col = 'report_date', parse_dates = ['report_date'])
                                
    # for date in localDayInWeek.index:
    #     purchaseRedeemPredictDayInWeek.ix[date] = localDayInWeek.ix[date]
    
    purchaseRedeemPredict.ix[localDayInWeek.index] = localDayInWeek
    multiErrorVarDayInWeek = purchaseRedeemModelEvaluate(purchaseRedeemPredict, ['day in week'])
    print ('day in week begin')
    print ('errorVar after single date: ')
    print ('purchaseErrorVar = ', multiErrorVarDayInWeek[0], 'redeemErrorVar = ', multiErrorVarDayInWeek[1])
    
    return (purchaseRedeemPredict, multiErrorVarDayInWeek)
    
def onlineMergeDayInWeek(purchaseRedeemPredict):
    purchaseRedeemPredictDayInWeek = purchaseRedeemPredict.copy()
    onlineDayInWeek = pd.read_csv('z:\\theblueisland\\raw_data\\onlineDayInWeek.csv', 
                                index_col = 'report_date', parse_dates = ['report_date'])
    purchaseRedeemPredictDayInWeek.ix[onlineDayInWeek.index] = onlineDayInWeek
    
    return purchaseRedeemPredictDayInWeek
    
def updateAndEvaluateArimaWeight():
    weight = DataFrame(index = modelTime, columns = ['purchaseWeight', 'redeemWeight'])
    testData = [1, 2]
    testData = [testData for _ in range(len(modelTime))]
    predict = {}
    errorVar = DataFrame(testData, index = modelTime, columns = ['purchaseError', 'redeemError'])
    
    # get model predict and errorVar
    print ()
    print ('updateAndEvaluateARIMAWeight')
    for dateSingle in modelTime:
        print (dateSingle)
        predictSingle, errorVarSingle = purchaseRedeemPredictLocalAndErrorVar(beginDate = dateSingle,
                                                                    order = modelOrder[dateSingle])
        print ()
        predict[dateSingle] = predictSingle
        errorVar.ix[dateSingle] = errorVarSingle
    errorVarSum = errorVar.sum()
    weight = ((errorVarSum - errorVar) / errorVarSum) / (len(modelTime) - 1)
    weight.index.name = 'report_date'
    weight.to_csv(arimaWeightFile)
    
    # evaluate assembly weight
    purchaseRedeemPredict = pd.DataFrame(index = pd.date_range('20140801', '20140831'),
                                        columns = ['purchasePredict', 'redeemPredict'])
    purchaseRedeemPredict.index.name = 'report_date'
    purchaseRedeemPredict.fillna(0, inplace = True)
    for dateSingle in modelTime:
        predictSingle = predict[dateSingle]
        weightSingle = weight.ix[dateSingle]
        purchaseRedeemPredict['purchasePredict'] += predictSingle[0] * weightSingle['purchaseError']
        purchaseRedeemPredict['redeemPredict'] += predictSingle[1] * weightSingle['redeemError']
    multiErrorVar = purchaseRedeemModelEvaluate(purchaseRedeemPredict, modelTime)
    print ('model weight: ')
    print (weight)
    print ('origin errorVar: ')
    print (errorVar)
    print ('errorVar after assembly: ')
    print ('purchaseErrorVar = ', multiErrorVar[0], 'redeemErrorVar = ', multiErrorVar[1])
    print ()
    
    # merge day in week
    #purchaseRedeemPredictDayInWeek, multiErrorVarDayInWeek = localMergeDayInWeek(purchaseRedeemPredict)
    #return (purchaseRedeemPredictDayInWeek, multiErrorVarDayInWeek)
    
    return (purchaseRedeemPredict, multiErrorVar)
# updateAndEvaluateArimaWeight()
    
def updateAndEvaluateGarchWeight():
    weight = DataFrame(index = modelTime, columns = ['purchaseWeight', 'redeemWeight'])
    testData = [1, 2]
    testData = [testData for _ in range(len(garchModelTime))]
    predict = {}
    errorVar = DataFrame(testData, index = garchModelTime, columns = ['purchaseError', 'redeemError'])
    
    # get model predict and errorVar
    print ()
    print ('updateAndEvaluateGARCHWeight')
    for dateSingle in garchModelTime:
        print (dateSingle)
        predictSingle, errorVarSingle = purchaseRedeemPredictLocalAndErrorVarGarch(beginDate = dateSingle,
                                                                    order = garchModelOrder[dateSingle])
        print ()
        predict[dateSingle] = predictSingle
        errorVar.ix[dateSingle] = errorVarSingle
    errorVarSum = errorVar.sum()
    weight = ((errorVarSum - errorVar) / errorVarSum) / (len(garchModelTime) - 1)
    weight.index.name = 'date'
    weight.to_csv(garchWeightFile)
    
    # evaluate assembly weight
    purchaseRedeemPredict = pd.DataFrame(index = pd.date_range('20140801', '20140831'),
                                        columns = ['purchasePredict', 'redeemPredict'])
    purchaseRedeemPredict.index.name = 'date'
    purchaseRedeemPredict.fillna(0, inplace = True)
    for dateSingle in garchModelTime:
        predictSingle = predict[dateSingle]
        weightSingle = weight.ix[dateSingle]
        purchaseRedeemPredict['purchasePredict'] += predictSingle[0] * weightSingle['purchaseError']
        purchaseRedeemPredict['redeemPredict'] += predictSingle[1] * weightSingle['redeemError']
    multiErrorVar = purchaseRedeemModelEvaluate(purchaseRedeemPredict, garchModelTime)
    
    print ('model weight: ')
    print (weight)
    print ()
    print ('origin errorVar: ')
    print (errorVar)
    print ('errorVar after assembly: ')
    print ('purchaseErrorVar = ', multiErrorVar[0], 'redeemErrorVar = ', multiErrorVar[1])

    return purchaseRedeemPredict, multiErrorVar
    
# updateAndEvaluateGarchWeight()

def assembleARIMAandGARCH():
    arimaPredict, arimaErrorVar = updateAndEvaluateArimaWeight()
    garchPredict, garchErrorvar = updateAndEvaluateGarchWeight()
    arimaErrorVar = [error for error in arimaErrorVar]
    garchErrorvar = [error for error in garchErrorvar]
    errorVar = DataFrame(index = [0, 1], columns = [0, 1])
    errorVar.ix[0] = arimaErrorVar
    errorVar.ix[1] = garchErrorvar
    errorVarSum = errorVar.sum()
    weight = ((errorVarSum - errorVar) / errorVarSum)
    weight.to_csv(weightArimaGarchFile)
    
    purchaseRedeemPredict = pd.DataFrame(index = pd.date_range('20140801', '20140831'),
                                        columns = ['purchasePredict', 'redeemPredict'])
    purchaseRedeemPredict.index.name = 'date'
    purchaseRedeemPredict.fillna(0, inplace = True)
    purchaseRedeemPredict['purchasePredict'] += arimaPredict['purchasePredict'] * weight.ix[0, 0]
    purchaseRedeemPredict['purchasePredict'] += garchPredict['purchasePredict'] * weight.ix[1, 0]
    purchaseRedeemPredict['redeemPredict'] += arimaPredict['redeemPredict'] * weight.ix[0, 1]
    purchaseRedeemPredict['redeemPredict'] += garchPredict['redeemPredict'] * weight.ix[1, 1]
    multiErrorVar = purchaseRedeemModelEvaluate(purchaseRedeemPredict, 'ARIMA and GARCH')
    
    print ('ARIMA and GARCH model weight: ')
    print (weight)
    print ('origin errorVar: ')
    print (errorVar)
    print ('errorVar after assembly ARIMA and GARCH: ')
    print ('purchaseErrorVar = ', multiErrorVar[0], 'redeemErrorVar = ', multiErrorVar[1])

# assembleARIMAandGARCH()

#dateSingle = '2014-05-01'
def arimaMultiModelOnline():
    weight = pd.read_csv(arimaWeightFile, index_col = 'report_date')
    purchaseRedeemPredict = pd.DataFrame(index = pd.date_range('20140901', '20140930'),
                                        columns = ['purchasePredict', 'redeemPredict'])
    purchaseRedeemPredict.index.name = 'date'
    purchaseRedeemPredict.fillna(0, inplace = True)
    print ()
    print ('arimaMultiModelOnline')
    for dateSingle in modelTime:
        print (dateSingle)
        purchasePredict, redeemPredict = purchaseRedeemPredictOnlineEasy(beginDate = dateSingle,
                                                                        order = modelOrder[dateSingle])
        print()
        weightSingle = weight.ix[dateSingle]
        purchaseRedeemPredict['purchasePredict'] += purchasePredict * weightSingle['purchaseError']
        purchaseRedeemPredict['redeemPredict'] += redeemPredict * weightSingle['redeemError']
    #purchaseRedeemPredictDayInWeek = onlineMergeDayInWeek(purchaseRedeemPredict)
    #return purchaseRedeemPredictDayInWeek
    return purchaseRedeemPredict
# arimaMultiModelOnline()
    
def garchMultiModelOnline():
    weight = pd.read_csv(garchWeightFile, index_col = 'date')
    purchaseRedeemPredict = pd.DataFrame(index = pd.date_range('20140901', '20140930'),
                                        columns = ['purchasePredict', 'redeemPredict'])
    purchaseRedeemPredict.index.name = 'date'
    purchaseRedeemPredict.fillna(0, inplace = True)
    print ()
    print ('garchMultiModelOnline')
    for dateSingle in garchModelTime:
        print (dateSingle)
        purchasePredict, redeemPredict = purchaseRedeemPredictOnlineEasyGarch(beginDate = dateSingle,
                                                                        order = garchModelOrder[dateSingle])
        print()
        weightSingle = weight.ix[dateSingle]
        purchaseRedeemPredict['purchasePredict'] += purchasePredict * weightSingle['purchaseError']
        purchaseRedeemPredict['redeemPredict'] += redeemPredict * weightSingle['redeemError']
    return purchaseRedeemPredict
    
def assembleARIMAandGARCHOnline():
    arimaPredict = arimaMultiModelOnline()
    garchPredict = garchMultiModelOnline()
    purchaseRedeemPredict = pd.DataFrame(index = pd.date_range('20140901', '20140930'),
                                        columns = ['purchasePredict', 'redeemPredict'])
    purchaseRedeemPredict.index.name = 'date'
    purchaseRedeemPredict.fillna(0, inplace = True)
    
    # use purcahse of garch and use redeem of arima
    # purchaseRedeemPredict['purchasePredict'] = garchPredict['purchasePredict']
    # purchaseRedeemPredict['redeemPredict'] = arimaPredict['redeemPredict']
    
    # weight of arima and garch
    weight = pd.read_csv(weightArimaGarchFile, index_col = [0])
    purchaseRedeemPredict['purchasePredict'] += arimaPredict['purchasePredict'] * weight.ix[0, 0]
    purchaseRedeemPredict['redeemPredict'] += arimaPredict['redeemPredict'] * weight.ix[0, 1]
    purchaseRedeemPredict['purchasePredict'] += garchPredict['purchasePredict'] * weight.ix[1, 0]
    purchaseRedeemPredict['redeemPredict'] += garchPredict['redeemPredict'] * weight.ix[1, 1]
    
    return purchaseRedeemPredict
    
# assembleARIMAandGARCHOnline()

#arimaMultiModelOnline()
    ## weight calculate which are not correct
    # errorVarPurchase =  np.dot(errorVar['purchaseError'], 
    #                             pd.concat([errorVar['purchaseError'] for _ in range(len(modelTime))],
    #                             axis = 1).T).sum()
    # errorVarRedeem =  np.dot(errorVar['redeemError'], 
    #                             pd.concat([errorVar['redeemError'] for _ in range(len(modelTime))],
    #                             axis = 1).T).sum()
    # for dateSingle in modelTime:
    #     #dateSingle = '2014-05-01'
    #     errorVarCopy = errorVar.copy()
    #     errorVarCopy.ix[dateSingle] = (0, 0)
    #     errorVarPurchaseSingle = np.dot(errorVar['purchaseError'], 
    #                             pd.concat([errorVarCopy['purchaseError'] for _ in range(len(modelTime))],
    #                             axis = 1).T).sum()
    #     errorVarRedeemSingle = np.dot(errorVarCopy['redeemError'], 
    #                             pd.concat([errorVarCopy['redeemError'] for _ in range(len(modelTime))],
    #                             axis = 1).T).sum()
    #     weight.ix[dateSingle] = (errorVarPurchaseSingle / errorVarPurchase, errorVarRedeem / errorVarRedeemSingle)