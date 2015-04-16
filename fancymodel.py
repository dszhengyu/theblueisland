from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cross_validation import StratifiedKFold, train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from datetime import datetime
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import f1_score, classification_report, precision_score
from sklearn.learning_curve import learning_curve
from sklearn.externals import joblib
from extractFeature_Pandas import featureName
from rockup import pwd

featureName = pwd + 'feature_name.csv'
featureScore = pwd + 'feature_score.csv'
prefix = pwd + "feature_label2\\"
model = pwd + 'model\\'

def getDates(beginDate, daycount):
    dateList = ['11' + '_' + str(day) for day in range(18, 31)]
    dateList += ['12' + '_' + str(day) for day in range(1, 9)]
    start = dateList.index(beginDate)
    return dateList[start : start + daycount]

def generateXy(beginDate, daycount):
# start time
    begin = datetime.now()
    print ('splict start ', begin)
#default use '12_8' as test set
    X_test = np.loadtxt(prefix + 'test_feature_12_8.csv', delimiter = ',')
    X_test = MinMaxScaler().fit_transform(X_test)
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
    X_train = MinMaxScaler().fit_transform(X_train)
#time
    end = datetime.now()
    print ('splict end ', end)
    print ('')
    return X_train, y_train
  
def modelFactory(option):
    clf1File = model + 'clfPickle1.plk'
    clf2File = model + 'clfPickle2.plk'
    clf3File = model + 'clfPickle3.plk'
    if (option == 'train'):
        clf1 = LogisticRegression(class_weight = 'auto')
        param1 = {'C' : [0.001, 0.03, 0.9, 27, 100, 300], 
                    'penalty' : ['l1', 'l2']}
        clf2 = RandomForestClassifier()
        param2 = {'n_estimators' : [i for i in range(50, 120, 30)]}
        clf3 = GradientBoostingClassifier()
        param3 = {'n_estimators' : [i for i in range(100, 200, 50)]}
        return [(clf1, param1, clf1File), (clf2, param2, clf2File), 
                    (clf3, param3, clf3File)]
    elif (option == 'predict'):
        clf1 = joblib.load(clf1File)
        clf1Score = 1
        clf2 = joblib.load(clf2File)
        clf2Score = 1
        clf3 = joblib.load(clf3File)
        clf3Score = 1
        return [(clf1, clf1Score), (clf2, clf2Score), (clf3, clf3Score)]
        
def gridTrain(X, y):
    begin = datetime.now()
    print ('training start ', begin)
    featureImportance = pd.read_csv(featureName)
    i = 0
    for clf, param, file in modelFactory('train'):
        clf = GridSearchCV(estimator = clf, param_grid = param, 
                        scoring = 'precision', n_jobs = 1, 
                        cv = StratifiedKFold(y, 3))
        clf.fit(X, y)
        clf = clf.best_estimator_
        try:
            featureImportance.loc[i] = clf.feature_importances_
        except Exception:
            pass
        else:
            i += 1
        y_pred = clf.predict(X)
        showLearningCurve(clf, X, y)
        joblib.dump(clf, file)
    featureImportance.loc['sum'] = featureImportance.sum()
    featureImportance = featureImportance.stack().unstack(0)
    featureImportance.sort_index(by = ['sum'], inplace = True)
    featureImportance.to_csv(featureScore)
    end = datetime.now()
    print ('training end ', end)
    print ('')

def showLearningCurve(clf, X, y):
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

def test():
    input(">> ")

if __name__ == '__main__': test()
