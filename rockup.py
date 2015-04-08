from extractFeature import extractFeature
from fancymodel import *

def updateFeature(begin = '11_18', days = 1, target = 0):
    f = open('update_feature_log.log', 'w')
    if (target):
        f.write('target updating... ')
        extractFeature('target ', 1)
        f.write('update complete\n')
        f.flush()
    daySet = getDates(begin, days)
    for d in daySet:
        f.write(d + ' updating... ')
        extractFeature(d, 0)
        f.write(d + ' update complete\n')
        f.flush()
    f.close()

def train(begin = '11_18', days = 1, option = 0, cv = 3):
    #split the data into train_cv & test
    X, y = splitTCT(begin, days)  
    #base on option, just train or grid_search or learning_curve
    if(option == 1):
        justTrain(X, y)
    elif (option == 2):
        gridTrain(X, y, cv)
    elif (option == 3):
        showLearningCurve(X, y, cv)
 
def localTest():   
    'test on the local date, which solit from function train()'
    X_test = np.load('X_test.npy')
    y_test = np.load('y_test.npy')
    clf = joblib.load('clfPickle.plk')
    #evalue the model
    y_pred = clf.predict(X_test)
    print classification_report(y_test, y_pred)
    
def onlineSet():
    #1 predict the y
    X = np.loadtxt('feature_label\\feature_target.csv', delimiter = ',')
    clf = joblib.load('clfPickle.plk')
    y = clf.predict(X)
    #2 get the predicted (user_id, item_id)
    online = np.loadtxt('feature_label\\example_target.csv',
                        delimiter = ',', dtype = 'S15')
    online = online[y > 0]
    #3 cross betaList and subItemDict
    subItemDict = {}
    l = open('data_version2\\subItem.csv')
    for line in l.readlines():
        entry = [elm.strip('"\n') for elm in line.split(",")]
        subItemDict[entry[0]] = None
    l.close()
    online2 = []
    for i in online:
        if i[1] in subItemDict:
            online2.append(i)
    online = online2
    #4 remove the repeate (user_id, item_id)
    online = [tuple(i) for i in online]
    online = list(set(online))
    #5 into file
    online = np.asarray(online, dtype = np.float32)
    np.savetxt(fname = 'tianchi_mobile_recommendation_predict.csv',
               X = online, delimiter = ',')
    onlineFile = open('tianchi_mobile_recommendation_predict.csv')
    content = onlineFile.readlines()
    onlineFile.close()
    onlineFile = open('tianchi_mobile_recommendation_predict.csv', 'w')
    onlineFile.write('user_id, item_id\n')
    onlineFile.writelines(content)
    onlineFile.close()


def main():
    print "1) updateFeature"
    print "2) train"
    print "3) localtest"
    print "4) onlinetest"
    menu = raw_input(">> ")
    if (menu == '1'):
        begin = raw_input("begin from.. or n for default ")
        days = raw_input("days .. or n for default ")
        target =  raw_input("target ? or n for default ")
        if (begin == 'n'):
            begin = '11_18'
        if (days == 'n'):
            days = 1
        else:
            days = int(days)
        if (target == 'n'):
            target = 0
        else:
            target = 1
        updateFeature(begin, days, target)
    if (menu == '2'):
        begin = raw_input("begin or n for default ")
        days = raw_input("days or n for default ")
        print "1) justTrain"
        print "2) gridTrain"
        print "3) showLearningCurve"
        option =  raw_input("option ")
        if (begin == 'n'):
            begin = '11_18'
        if (days == 'n'):
            days = 1
        else:
            days = int(days)
        option = int(option)
        train(begin, days, option)
    if (menu == '3'):
        localtest()
    if (menu == '4'):        
        onlineSet()
        
def unitTest4localTest():
    train_date = '11_18'
    train_days = 3
    test_date = '11_21'
    test_days = 1
    localTest(train_date, train_days, test_date, test_days)


def test():
##    train('11_18', 7, 2)
##    localTest()
    onlineSet()

if __name__ == '__main__': test()
