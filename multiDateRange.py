import numpy as np
import pandas as pd
from pandas import DataFrame

from easyRude import purchaseRedeemPredictErrorVar
pwd = 'z:\\theblueisland\\'
arimaWeightFile = pwd + 'arimaWeightFile.csv'
modelTime = ['2013-07-01', '2013-09-01', '2013-11-01', '2014-03-01', '2014-05-01']

def updateArimaWeight():
    weight = DataFrame(index = modelTime, columns = ['purchaseWeight', 'redeemWeight'])
    testData = [1, 2]
    testData = [testData for _ in range(len(modelTime))]
    errorVar = DataFrame(testData, index = modelTime, columns = ['purchaseError', 'redeemError'])
    
    for dateSingle in modelTime:
        #dateSingle = '2014-05-01'
        errorVarSingle = purchaseRedeemPredictErrorVar(beginDate = dateSingle)
        errorVar.ix[dateSingle] = errorVarSingle
    errorVarSum = errorVar.sum()
    weight = ((errorVarSum - errorVar) / errorVarSum) / (len(modelTime) - 1)
    weight.index.name = 'date'
    weight.to_csv(arimaWeightFile)
    
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
    
def evaluateArimaWeight():
    weight = pd.read_csv(arimaWeightFile, index_col = ['date'])