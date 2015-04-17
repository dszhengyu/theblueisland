from extractFeature import extractFeature
from fancymodel import *
from extractFeature_Pandas import extractFeature_Pandas
from damnrule import ruleFile

pwd = 'z:\\theblueisland\\'
ruleScore = 1
trainthreshold = 3
onlineThreshold = 3

def updateFeature(begin = '11_18', days = 1, target = 0):
    f = open('update_feature_log.log', 'w')
    if (target):
        f.write('target updating... ')
        extractFeature_Pandas('target ', random = 0, target = 1)
        f.write('update complete\n')
        f.flush()
    daySet = getDates(begin, days)
    for d in daySet:
        f.write(d + ' updating... ')
        extractFeature_Pandas(d)
        f.write(d + ' update complete\n')
        f.flush()
    f.close()

def train(begin = '11_18', days = 1):
    X, y = generateXy(begin, days)  
    gridTrain(X, y)
 
def localTest():   
    'test on the local set'
    X_test = np.load(pwd + 'X_test.npy')
    y_test = np.load(pwd + 'y_test.npy')
    y = pd.DataFrame(index = range(len(X_test)))
    clf, score= modelFactory('predict')[0]
    y_pred = clf.predict(X_test)
    y_pred = np.logical_and(y_pred, y_pred)
    i = 1
    y.loc[y_pred, i] = score
    print (clf)
    print ('y_pred: ' + str(y_pred.sum()))
    print (classification_report(y_test, y_pred))
    print ('')
    for clf, score in modelFactory('predict')[1 : ]:
        y_pred = clf.predict(X_test)
        y_pred = np.logical_and(y_pred, y_pred)
        i += 1
        y.loc[y_pred, i] = score
        print (clf)
        print ('y_pred: ' + str(y_pred.sum()))
        print (classification_report(y_test, y_pred))
        print ('')
    y.fillna(value = 0, inplace = True)
    y = y.sum(axis = 1) >= trainthreshold
    print ('final predict:')
    print ('y_pred: ' + str(y.sum()))
    print (classification_report(y_test, y))
    
def onlineSet(norule = 1):
    index = ['user_id', 'item_id']
    #1 predict the y_pred
    X = pd.read_csv(prefix + 'feature_target.csv', header = None)
    X = MinMaxScaler().fit_transform(X)
    # y = pd.DataFrame(index = range(len(X)))
    y = pd.read_csv(prefix + 'example_target.csv', names = index)
    clf, score = modelFactory('predict')[0]
    y_pred = clf.predict(X)
    y_pred = np.logical_and(y_pred, y_pred)
    i = 1
    y.loc[y_pred, i] = score
    print (y_pred.sum())
    for clf, score in modelFactory('predict')[1 : ]:
        y_pred = clf.predict(X)
        y_pred = np.logical_and(y_pred, y_pred)
        i += 1
        y.loc[y_pred, i] = score
        print (y_pred.sum())
    y.fillna(value = 0, inplace = True)
    print ('online set before rule: ' 
            + str((y.ix[ : , 1 :].sum(axis = 1) >= onlineThreshold).sum()))
    # add rule
    if (norule == 0):
        rule = pd.read_csv(ruleFile, names = ['user_id', 'item_id'])
        rule['rule'] = ruleScore
        y = pd.merge(y, rule, how = 'outer')
        y.fillna(value = 0, inplace = True)
    # threshold, get online
    online = y[y.ix[ : , 1 :].sum(axis = 1) >= onlineThreshold]
    online = online.ix[ : , 'user_id' : 'item_id']
    print ('online set before cross: ' + str(len(online)))
    # cross the subItem set
    l = pd.read_csv(pwd + 'data_version2\\subItem.csv', 
                        names = ['item_id', 'item_category'])
    online = pd.merge(online, l)
    # remove the repeat (user_id, item_id)
    online.drop_duplicates(inplace = True)
    print ('online set final: ' + str(len(online)))
    # into file
    online.ix[ :, : -1].to_csv(pwd + 'tianchi_mobile_recommendation_predict.csv', 
                                na_rep = '0', index = False, header = True)

def test():
    updateFeature('11_18', 10)
    extractFeature_Pandas('12_8', 0)
    extractFeature_Pandas('target', target = 1)
    train('11_18', 10)
    localTest()
    onlineSet()
    
def main():
    updateFeature('11_18', 21)
    extractFeature_Pandas('12_8', 0)
    extractFeature_Pandas('target', target = 1)
    train('11_18', 20)
    localTest()
    train('11_18', 21)
    onlineSet()

if __name__ == '__main__': test()
