import numpy as np
import pandas as pd
from pandas import DataFrame

from easyRude import purchaseRedeemPredictLocalAndErrorVar, purchaseRedeemModelEvaluate, purchaseRedeemPredictOnlineEasy
from easyRude import purchaseRedeemPredictLocalAndErrorVarGarch, purchaseRedeemPredictOnlineEasyGarch
pwd = 'z:\\theblueisland\\'
arimaWeightFile = pwd + 'arimaWeightFile.csv'
modelTime = ['2013-11-01', '2014-03-01', '2014-04-01']
modelOrder = {'2013-11-01' : ([8, 1, 8], [14, 1, 14]),
                '2014-03-01' : ([12, 1, 12], [6, 1, 7]),
                '2014-04-01' : ([13, 1, 14], [13, 1, 14])}
# modelTime = ['2013-11-01', '2014-03-01', '2014-04-01', '2014-05-01']
# modelOrder = {'2013-11-01' : ([8, 1, 8], [14, 1, 14]),
#                 '2014-03-01' : ([12, 1, 12], [6, 1, 7]),
#                 '2014-04-01' : ([13, 1, 14], [13, 1, 14]),
#                 '2014-05-01' : ([12, 2, 12], [14, 1, 15])}
                
garchWeightFile = pwd + 'garchWeightFile.csv'  
garchModelTime = ['2013-11-01', '2014-03-01']
garchModelOrder = { '2013-11-01' : ([20, 3], [8, 8]),
                '2014-03-01' : ([8, 7], [7, 8])}          
# garchModelTime = ['2013-07-01', '2013-11-01', '2014-03-01', '2014-04-01']
# garchModelOrder = {'2013-07-01' : ([20, 3], [20, 8]),
#                 '2013-11-01' : ([20, 3], [8, 8]),
#                 '2014-03-01' : ([8, 7], [7, 8]),
#                 '2014-04-01' : ([7, 11], [8, 10])}
                
weightArimaGarchFile = pwd + 'weightArimaGarchFile.csv'

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
    weight.index.name = 'date'
    weight.to_csv(arimaWeightFile)
    
    # evaluate assembly weight
    purchaseRedeemPredict = pd.DataFrame(index = pd.date_range('20140801', '20140831'),
                                        columns = ['purchasePredict', 'redeemPredict'])
    purchaseRedeemPredict.index.name = 'date'
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
    weight = pd.read_csv(arimaWeightFile, index_col = 'date')
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
    return purchaseRedeemPredict
    
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