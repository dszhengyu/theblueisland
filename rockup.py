from extractFeature import extractFeature
from fancymodel import *
from extractFeature_Pandas import extractFeature_Pandas

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
    X_test = np.load('X_test.npy')
    y_test = np.load('y_test.npy')
    clf = modelFactory('predict')[0]
    y = clf.predict(X_test)
    y = np.logical_and(y, y)
    print (clf)
    print ('y_pred: ' + str(y.sum()))
    print (classification_report(y_test, y))
    print ('')
    for clf in modelFactory('predict')[1 : ]:
        y_pred = clf.predict(X_test)
        y = np.logical_and(y, y_pred)
        print (clf)
        print ('y_pred: ' + str(y_pred.sum()))
        print (classification_report(y_test, y_pred))
        print ('')
    print ('final predict:')
    print (classification_report(y_test, y))
    
def onlineSet():
    index = ['user_id', 'item_id']
    #1 predict the y
    X = pd.read_csv(prefix + 'feature_target.csv', header = None)
    X = MinMaxScaler().fit_transform(X)
    clf = modelFactory('predict')[0]
    y = clf.predict(X)
    y = np.logical_and(y, y)
    print (y.sum())
    for clf in modelFactory('predict')[1 : ]:
        y1 = clf.predict(X)
        print (y1.sum())
        y = np.logical_and(y, y1)
    print ('y_pred: ' + str(y.sum()))
    #2 get the predicted (user_id, item_id)
    online = pd.read_csv(prefix + 'example_target.csv', names = index)
    online1 = online[y]
    #3 cross betaList and subItemDict
    l = pd.read_csv(pwd + 'data_version2\\subItem.csv', 
                        names = ['item_id', 'item_category'])
    online1 = pd.merge(online1, l)
    #4 remove same category
    
    #5 remove the repeate (user_id, item_id)
    online1 = online1.drop_duplicates()
    #6 into file
    print ('online set: ' + str(len(online1)))
    online1.ix[ :, : -1].to_csv(pwd + 'tianchi_mobile_recommendation_predict.csv', 
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
