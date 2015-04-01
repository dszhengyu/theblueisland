import numpy as np
import cPickle as pickle
from sklearn.linear_model import LogisticRegression
from datetime import datetime

prefix = "Z:\\theblueisland\\feature_label\\"

def getDates(beginDate, daycount):
    dateList = ['11' + '_' + str(day) for day in range(18, 31)]
    dateList += ['12' + '_' + str(day) for day in range(1, 19)]
    start = dateList.index(beginDate)
    return dateList[start : start + daycount]

def trainModel(train_date, train_days):
    'method to train the model'
    daySet = getDates(train_date, train_days)
    trainDaySet = [prefix + 'feature_'+ f + '.csv' for f in daySet]
    labelDaySet = [prefix + 'label_'+ f + '.csv' for f in daySet]
    X = np.loadtxt(trainDaySet[0], delimiter = ',')
    y = np.loadtxt(labelDaySet[0], delimiter = ',')
    if (train_days > 1):
        for f in trainDaySet[1 : ]:
            X = np.vstack((X, np.loadtxt(f, delimiter = ',')))
        for f in labelDaySet[1 : ]:
            y = np.vstack((y, np.loadtxt(f, delimiter = ',')))
    lr = LogisticRegression(C = 1.0)
    lr.fit(X, y)
    lrFile = open('lrPickle.plk', 'wb')
    pickle.dump(lr, lrFile, 1)
    lrFile.close()
    return lr

def predict(test_date, test_days, target = 0):
    'use model to predict and get hypothesis'
    if (target == 0):
        daySet = getDates(test_date, test_days)
        testDaySet = [prefix + 'feature_'+ f + '.csv' for f in daySet]
        X = np.loadtxt(testDaySet[0], delimiter = ',')
        if (test_days > 1):
            for f in testDaySet[1 : ]:
                X = np.vstack((X, np.loadtxt(f, delimiter = ',')))
    else:
        X = np.loadtxt(prefix + 'feature_target.csv', delimiter = ',')      
    lrFile = open('lrPickle.plk', 'rb')
    lr = pickle.load(lrFile)
    hypothesis = lr.predict(X)
    lrFile.close()
    np.save('hypothesis.npy', hypothesis)
    return hypothesis

def analyseHypothesis(test_date, test_days, hypothesis, threshhold = 0):
    'get precision, recall and F1'
    #1 use testDaySet to form real target, and put into targetDict
    daySet = getDates(test_date, test_days)
    testDaySet = [prefix + 'label_'+ f + '.csv' for f in daySet]
    y = np.loadtxt(testDaySet[0], delimiter = ',')
    if (test_days > 1):
        for f in testDaySet[1 : ]:
            y = np.vstack((y, np.loadtxt(f, delimiter = ',')))
    #2 according to threshhold to judge and see in targetDict or not
    #  get precision, recall
    y = np.asarray(y, dtype = 'bool')
    finalGuess = hypothesis > threshhold
    predict_num = finalGuess.sum(0)
    total_brand = y.sum(0)
    hit = (finalGuess & y).sum(0) 
    #3 caulate F1
    precision = float(hit) / predict_num
    recall = float(hit) / total_brand
    F1 = 2 * precision * recall / (precision + recall)
    error = (finalGuess != y).sum(0) / float(y.shape[0])
    return precision, recall, F1, error


def test():
    print datetime.now()
    #hypothesis = predict('11_19', 1)
    hypothesis = np.load('hypothesis.npy')
    p, r, f, error= analyseHypothesis('11_19', 1, hypothesis)
    print p, r, f, error
    print datetime.now()
    input(">> ")

if __name__ == '__main__': test()
