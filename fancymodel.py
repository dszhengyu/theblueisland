import numpy as np
from sklearn.cross_validation import StratifiedKFold, train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.linear_model import LogisticRegression
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import f1_score, classification_report
from sklearn.learning_curve import learning_curve
from sklearn.externals import joblib

prefix = "feature_label\\"

def getDates(beginDate, daycount):
    dateList = ['11' + '_' + str(day) for day in range(18, 31)]
    dateList += ['12' + '_' + str(day) for day in range(1, 19)]
    start = dateList.index(beginDate)
    return dateList[start : start + daycount]

def splitTCT(beginDate, daycount):
    'method to train the model'
    daySet = getDates(beginDate, daycount)
    trainDaySet = [prefix + 'feature_'+ f + '.csv' for f in daySet]
    labelDaySet = [prefix + 'label_'+ f + '.csv' for f in daySet]
    X = np.loadtxt(trainDaySet[0], delimiter = ',')
    y = np.loadtxt(labelDaySet[0], delimiter = ',')

    for f in trainDaySet[1 : ]:
        X = np.vstack((X, np.loadtxt(f, delimiter = ',')))
    for f in labelDaySet[1 : ]:
        #y = np.vstack((y, np.loadtxt(f, delimiter = ',')))
        y = y.tolist()
        y1 = np.loadtxt(f, delimiter = ',').tolist()
        y.extend(y1)
        y = np.array(y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
    X_test = StandardScaler().fit_transform(X_test)
    np.save('X_test.npy', X_test)
    np.save('y_test.npy', y_test)
    X_train = StandardScaler().fit_transform(X_train)
    
    return X_train, y_train

def justTrain(X, y):
    clf = joblib.load('clfPickle.plk')
    clf.fit(X, y)
    joblib.dump(clf, 'clfPickle.plk')

def gridTrain(X, y, cv):
    parameters ={'penalty' : ['l1', 'l2'],
                 'C' : [0.001, 10000, 30]}
    clf = LogisticRegression()
    clf = GridSearchCV(estimator = clf, param_grid = parameters, scoring = 'f1',
                       n_jobs = 1, cv = StratifiedKFold(y, 3))
    clf.fit(X, y)
    joblib.dump(clf.best_estimator_, 'clfPickle.plk')
    print clf.best_estimator_

def showLearningCurve(X, y, cv):
    clf = joblib.load('clfPickle.plk')
    train_sizes, train_scores, valid_scores = learning_curve(clf, X, y,
                                                             cv = StratifiedKFold(y, 3),
                                                             n_jobs = 1)
    print train_sizes
    print train_scores
    print valid_scores

def test():
    X, y = splitTCT('11_18', 2)
    print X.shape[0]
    print ""
    print y.shape[0]
    input(">> ")

if __name__ == '__main__': test()
