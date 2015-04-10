import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cross_validation import StratifiedKFold, train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.linear_model import LogisticRegression
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import f1_score, classification_report
from sklearn.learning_curve import learning_curve
from sklearn.externals import joblib

pwd = 'z:\\theblueisland\\'
prefix = pwd + "feature_label\\"

def getDates(beginDate, daycount):
    dateList = ['11' + '_' + str(day) for day in range(18, 31)]
    dateList += ['12' + '_' + str(day) for day in range(1, 8)]
    start = dateList.index(beginDate)
    return dateList[start : start + daycount]

def generateXy(beginDate, daycount):
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

#default use '12_8' as test set
    X_test = np.loadtxt(prefix + 'feature_12_8.csv', delimiter = ',')
    y_test = np.loadtxt(prefix + 'label_12_8.csv', delimiter = ',')
    X_test = StandardScaler().fit_transform(X_test)
    np.save('X_test.npy', X_test)
    np.save('y_test.npy', y_test)
    
    X_train = X
    y_train = y
    
#qian gui ze complete

    X_train = StandardScaler().fit_transform(X_train)
    
    return X_train, y_train

def justTrain(X, y):
    clf = joblib.load(pwd + 'clfPickle.plk')
    clf.fit(X, y)
    joblib.dump(clf, 'clfPickle.plk')

def gridTrain(X, y, cv):
    parameters ={'penalty' : ['l1', 'l2'],
                 'C' : [0.001, 10000, 30]}
    clf = LogisticRegression()
    clf = GridSearchCV(estimator = clf, param_grid = parameters, scoring = 'f1',
                       n_jobs = 1, cv = StratifiedKFold(y, 3))
    clf.fit(X, y)
    joblib.dump(clf.best_estimator_, pwd + 'clfPickle.plk')
    print (clf.best_estimator_)
    showLearningCurve(X, y, cv)

def showLearningCurve(X, y, cv):
    clf = joblib.load(pwd + 'clfPickle.plk')
    train_sizes, train_scores, valid_scores = learning_curve(clf, X, y,
                                                             cv = StratifiedKFold(y, 3),
                                                             n_jobs = 1)
    plt.figure()
    plt.title('learning curve')
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    valid_scores_mean = np.mean(valid_scores, axis=1)
    valid_scores_std = np.std(valid_scores, axis=1)
    plt.grid()
    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, valid_scores_mean - valid_scores_std,
                     valid_scores_mean + valid_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, valid_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    plt.show()
    
    
    print (train_sizes)
    print (train_scores)
    print (valid_scores)

def test():
    print (X.shape[0])
    print ("")
    print (y.shape[0])
    input(">> ")

if __name__ == '__main__': test()
