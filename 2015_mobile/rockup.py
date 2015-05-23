from extractFeature import extractFeature
from fancymodel import *
from extractFeature_Pandas import extractFeature_Pandas
# from damnrule import ruleFile

pwd = 'z:\\theblueisland\\2015_mobile\\'
onlineset = pwd + 'onlineset\\'
ruleScore = 1
trainthreshold = 3
onlineThreshold = 3
item_trainthreshold = 2
item_threshold = 2

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

def train(begin = '11_18', days = 2):
    X, y = generateXy(begin, days)  
    gridTrain(X, y)
    item_X, item_y = item_generateXY(begin, days)
    item_gridTrain(item_X, item_y)
 
def localTest():   
    'test on the local set'
    # original test on <u, i>
    index = ['user_id', 'item_id']
    X_test = np.load(pwd + 'X_test.npy')
    y_test = np.load(pwd + 'y_test.npy')
    y = pd.read_csv(prefix + "test_example_12_8.csv", names = index)
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
    y['yes'] = 0
    y.ix[y.ix[ : , 1 :].sum(axis = 1) >= trainthreshold, 'yes'] = 1
    print ('final predict:')
    print ('y_pred: ' + str(y['yes'].sum()))
    print (classification_report(y_test, y['yes']))
    
    #test on <i>
    item_X_test = np.load(pwd + 'item_X_test.npy')
    item_y_test = np.load(pwd + 'item_y_test.npy')
    clf, score= item_modelFactory('predict')[0]
    item_y_pred = clf.predict(item_X_test)
    item_y_pred = np.logical_and(item_y_pred, item_y_pred)
    i = 1
    item_y = pd.read_csv(prefix + "test_item_label12_8.csv")
    item_y.drop('buy', inplace = True, axis = 1) 
    item_y.loc[item_y_pred, i] = score
    print (clf)
    print ('item_y_pred: ' + str(item_y_pred.sum()))
    print (classification_report(item_y_test, item_y_pred))
    print ('')
    for clf, score in item_modelFactory('predict')[1 : ]:
        item_y_pred = clf.predict(item_X_test)
        item_y_pred = np.logical_and(item_y_pred, item_y_pred)
        i += 1
        item_y.loc[item_y_pred, i] = score
        print (clf)
        print ('item_y_pred: ' + str(item_y_pred.sum()))
        print (classification_report(item_y_test, item_y_pred))
        print ('')
    item_y.fillna(value = 0, inplace = True)
    item_y['yes2'] = 0
    item_y.ix[item_y.ix[ : , 1 :].sum(axis = 1) >= item_trainthreshold, 'yes2'] = 1
    print ('item_final predict:')
    print ('item_y_pred: ' + str(item_y['yes2'].sum()))
    print (classification_report(item_y_test, item_y['yes2']))
    
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
    print ('online cross with subitem: ' + str(len(online)))
    
    ## item
    item_X =  pd.read_csv(prefix + 'item_feature_targettarget.csv', index_col = 'item_id')
    item_y = pd.DataFrame(index = item_X.index)
    item_X = MinMaxScaler().fit_transform(item_X)
    
    clf, score= item_modelFactory('predict')[0]
    item_y_pred = clf.predict(item_X)
    item_y_pred = np.logical_and(item_y_pred, item_y_pred)
    i = 1
    item_y.loc[item_y_pred, i] = score
    print (clf)
    print ('item_y_pred: ' + str(item_y_pred.sum()))
    print ('')
    for clf, score in item_modelFactory('predict')[1 : ]:
        item_y_pred = clf.predict(item_X)
        item_y_pred = np.logical_and(item_y_pred, item_y_pred)
        i += 1
        item_y.loc[item_y_pred, i] = score
        print (clf)
        print ('item_y_pred: ' + str(item_y_pred.sum()))
        print ('')
    item_y.fillna(value = 0, inplace = True)
    item_y['yes'] = 0
    item_y.ix[item_y.ix[ : , 1 :].sum(axis = 1) >= item_threshold, 'yes'] = 1
    item_y.fillna(value = 0, inplace = True)
    finalItem = pd.DataFrame(index = item_y[item_y['yes'] != 0].index)
    print ('item_y_pred final: ' + str(len(finalItem)))
    
    # online = pd.merge(online, finalItem, left_on = 'item_id', right_index = True)
    ##item
    
    print ('online set final: ' + str(len(online)))
    # into file
    online.ix[ :, : -1].to_csv(pwd + 'tianchi_mobile_recommendation_predict.csv', 
                                na_rep = '0', index = False, header = True)
    online.ix[ :, : -1].to_csv(onlineset + str(len(online)) + '@@' +
                                str(datetime.now()).replace(':', '-') + '.csv',  
                                na_rep = '0', index = False, header = True)                    

def test():
    # updateFeature('11_18', 15)
    # extractFeature_Pandas('12_8', test = 1)
    # extractFeature_Pandas('target', target = 1)
    train('11_18', 15)
    # localTest()
    # onlineSet()
    
def main():
    updateFeature('11_18', 21)
    extractFeature_Pandas('12_8', 0)
    extractFeature_Pandas('target', target = 1)
    train('11_18', 20)
    localTest()
    train('11_18', 21)
    onlineSet()

if __name__ == '__main__': test()
