import numpy as np
import pandas as pd
from pandas import DataFrame

from easyRude import purchaseRedeemPredictLocalAndErrorVar, purchaseRedeemModelEvaluate, purchaseRedeemPredictOnlineEasy
pwd = 'z:\\theblueisland\\'
arimaWeightFile = pwd + 'arimaWeightFile.csv'
modelTime = ['2013-07-01', '2013-09-01', '2013-11-01', '2014-03-01', '2014-05-01']
modelOrder = {'2013-07-01' : ([8, 1, 8], [12, 1, 12]),
                '2013-09-01' : ([12, 1, 12], [15, 1, 15]),
                '2013-11-01' : ([8, 1, 8], [14, 1, 14]),
                '2014-03-01' : ([12, 1, 12], [6, 1, 7]),
                '2014-05-01' : ([12, 2, 12], [10, 2, 14])}
def updateAndEvaluateArimaWeight():
    weight = DataFrame(index = modelTime, columns = ['purchaseWeight', 'redeemWeight'])
    testData = [1, 2]
    testData = [testData for _ in range(len(modelTime))]
    predict = {}
    errorVar = DataFrame(testData, index = modelTime, columns = ['purchaseError', 'redeemError'])
    
    # get model predict and errorVar
    print ()
    print ('updateAndEvaluateArimaWeight')
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

    return purchaseRedeemPredict
    
#updateAndEvaluateArimaWeight()
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