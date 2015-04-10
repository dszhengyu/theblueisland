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
    trainAll(X, y)
 
def localTest():   
    'test on the local date, which solit from function train()'
    X_test = np.load('X_test.npy')
    y_test = np.load('y_test.npy')
    clf1 = joblib.load(clf1File)
    #evalue the model
    y_pred1 = clf1.predict(X_test)
    print (classification_report(y_test, y_pred1))
    
def onlineSet():
    index = ['user_id', 'item_id']
    #1 predict the y
    X = pd.read_csv(prefix + 'feature_target.csv', header = None)
    clf1 = joblib.load(clf1File)
    y1 = clf1.predict(X)
    #2 get the predicted (user_id, item_id)
    online = pd.read_csv(prefix + 'example_target.csv', names = index)
    online1 = online[y1 > 0]
    #3 cross betaList and subItemDict
    l = pd.read_csv(pwd + 'data_version2\\subItem.csv', 
                        names = ['item_id', 'item_category'])
    online1 = pd.merge(online1, l)
    #4 remove same category

    #5 remove the repeate (user_id, item_id)
    online1 = online1.drop_duplicates()
    #6 into file
    online1.ix[ :, : -1].to_csv(pwd + 'tianchi_mobile_recommendation_predict.csv', 
                                na_rep = '0', index = False, header = True)

def main():
    print ("1) updateFeature")
    print ("2) train")
    print ("3) localtest")
    print ("4) onlinetest")
    menu = input(">> ")
    if (menu == '1'):
        begin = input("begin from.. or n for default ")
        days = input("days .. or n for default ")
        target =  input("target ? or n for default ")
        if (begin == 'n'):
            begin = '11_18'
        if (days == 'n'):
            days = 1
        else:
            days = int(days)
        if (target == 'n'):
            target = 0
        else:
            target = 12
        updateFeature(begin, days, target)
    if (menu == '2'):
        begin = input("begin or n for default ")
        days = input("days or n for default ")
        print ("1) justTrain")
        print ("2) gridTrain")
        option =  input("option ")
        if (begin == 'n'):
            begin = '11_18'
        if (days == 'n'):
            days = 1
        else:
            days = int(days)
        option = int(option)
        train(begin, days, option)
    if (menu == '3'):
        localTest()
    if (menu == '4'):        
        onlineSet()

def test():
    updateFeature('11_18', 20)
    extractFeature_Pandas('12_8', 0)
    extractFeature_Pandas('target', target = 1)
    train('11_18', 20)
    localTest()
    onlineSet()

if __name__ == '__main__': test()
