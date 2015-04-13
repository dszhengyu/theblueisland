import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cross_validation import StratifiedKFold, train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import f1_score, classification_report, precision_score
from sklearn.learning_curve import learning_curve
from sklearn.externals import joblib

pwd = 'z:\\theblueisland\\'
prefix = pwd + "feature_label2\\"

def getDates(beginDate, daycount):
    dateList = ['11' + '_' + str(day) for day in range(18, 31)]
    dateList += ['12' + '_' + str(day) for day in range(1, 9)]
    start = dateList.index(beginDate)
    return dateList[start : start + daycount]

def generateXy(beginDate, daycount):
    'method to train the model'
#default use '12_8' as test set
    X_test = np.loadtxt(prefix + 'test_feature_12_8.csv', delimiter = ',')
    X_test = StandardScaler().fit_transform(X_test)
    np.save('X_test.npy', X_test)
    y_test = np.loadtxt(prefix + 'test_label_12_8.csv', delimiter = ',')
    np.save('y_test.npy', y_test)
# train an cv set
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
    X_train = X
    y_train = y
#qian gui ze complete
    X_train = StandardScaler().fit_transform(X_train)
    return X_train, y_train
  
def modelFactory(option):
    clf1File = pwd + 'clfPickle1.plk'
    clf2File = pwd + 'clfPickle2.plk'
    # clf3File = pwd + 'clfPickle3.plk'
    if (option == 'train'):
        clf1 = LogisticRegression()
        param1 = {'C' : [0.001, 10000, 30], 'penalty' : ['l1', 'l2']}
        # clf2 = svm.LinearSVC(class_weight = 'auto')   
        # param2 = {'C' : [0.001, 10000, 30]}
        # clf3 = svm.SVC(cache_size = 1024)
        # param3 = {'C' : [0.001, 10000, 30], 'kernel' : ['rbf', 'sigmoid', 'limear']}
        return [(clf1, param1, clf1File)]#, (clf2, param2, clf2File)]
    elif (option == 'predict'):
        clf1 = joblib.load(clf1File)
        # clf2 = joblib.load(clf2File)
        # clf3 = joblib.load(clf3File)
        return [clf1]#, clf2]
        
def gridTrain(X, y):
    for clf, param, file in modelFactory('train'):
        clf = GridSearchCV(estimator = clf, param_grid = param, scoring = 'f1',
                        n_jobs = 1, cv = StratifiedKFold(y, 3))
        clf.fit(X, y)
        clf = clf.best_estimator_
        showLearningCurve(clf, X, y)
        joblib.dump(clf, file)

def showLearningCurve(clf, X, y):
    print (clf)
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
    # print (train_sizes)
    # print (train_scores)
    # print (valid_scores)

def test():
    input(">> ")

if __name__ == '__main__': test()
