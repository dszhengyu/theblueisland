from extractFeature import extractFeature
from fancymodel import *

def updateFeature(begin = '11_18', days = 1, target = 0):
    if (target):
        extractFeature('target ', 1)
    daySet = getDates(begin, days)
    for d in daySet:
        extractFeature(d, 0)
        
def localTest(train_date, train_days, test_date, test_days):   
    trainModel(train_date, train_days)
    hypothesis = predict(test_date, test_days)
    precision, recall, F1 = analyseHypothesis(test_date, test_days, hypothesis)
    print 'precision: ',  precision
    print 'recall: ', recall
    print 'F1: ', F1

def onlineSet(threshhold = 0):
    #hypothesis = predict('', 0, 1)
    hypothesis = np.load('hypothesis.npy')
    #1 get beta set according to threshhold, betaList
    finalGuess = hypothesis > threshhold
    #2 load subItemSet into subItemDict
    online = np.loadtxt('feature_label\\example_target.csv', delimiter = ',', dtype = 'S15')
    online2 = online[finalGuess]
    #3 cross betaList and subItemDict
    labelDict = {}
    l = open('data_version2\\i_target.csv')
    for line in l.readlines():
        entry = [elm.strip('"\n') for elm in line.split(",")]
        labelDict[(entry[0], entry[1])] = None
    l.close()
    onlineFile = open('online.csv', 'w')
    for i in online2:
        if (i[0], i[1]) in labelDict:
            onlineFile.write(','.join(i) + '\n')

def unitTest4localTest():
    train_date = '11_18'
    train_days = 3
    test_date = '11_21'
    test_days = 1
    localTest(train_date, train_days, test_date, test_days)


def test():
    onlineSet()
##    test_date = '11_19'
##    test_days = 1
##    hypothesis = predict(test_date, test_days)
##    precision, recall, F1 = analyseHypothesis(test_date, test_days, hypothesis)
##    print 'precision: ',  precision
##    print 'recall: ', recall
##    print 'F1: ', F1



if __name__ == '__main__': test()
