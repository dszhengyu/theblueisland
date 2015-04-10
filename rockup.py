from extractFeature import extractFeature
from fancymodel import *
from extractFeature_Pandas import extractFeature_Pandas

pwd = 'z:\\theblueisland\\'

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

def train(begin = '11_18', days = 1, option = 2, cv = 3):
    #split the data into train_cv & test
    X, y = generateXy(begin, days)  
    #base on option, just train or grid_search or learning_curve
    if(option == 1):
        justTrain(X, y)
    elif (option == 2):
        gridTrain(X, y, cv)
 
def localTest():   
    'test on the local date, which solit from function train()'
    X_test = np.load('X_test.npy')
    y_test = np.load('y_test.npy')
    clf = joblib.load('clfPickle.plk')
    #evalue the model
    y_pred = clf.predict(X_test)
    print (classification_report(y_test, y_pred))
    
def onlineSet():
    index = ['user_id', 'item_id']
    #1 predict the y
    X = pd.read_csv(pwd + 'feature_label\\feature_target.csv', header = None)
    clf = joblib.load(pwd + 'clfPickle.plk')
    y = clf.predict(X)
    #2 get the predicted (user_id, item_id)
    online = pd.read_csv(pwd + 'feature_label\\example_target.csv', names = index)
    online = online[y > 0]
    #3 cross betaList and subItemDict
    l = pd.read_csv(pwd + 'data_version2\\subItem.csv', 
                        names = ['item_id', 'item_category'])
    online = pd.merge(online, l)
    #4 remove same category

    #5 remove the repeate (user_id, item_id)
    online = online.drop_duplicates()
    #6 into file
    online.ix[ :, : -1].to_csv(pwd + 'tianchi_mobile_recommendation_predict.csv', 
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
        
def unitTest4localTest():
    train_date = '11_18'
    train_days = 3
    test_date = '11_21'
    test_days = 1
    localTest(train_date, train_days, test_date, test_days)


def test():
    # updateFeature('11_18', 21)
    # train('11_19', 19)
    # localTest()
    onlineSet()

if __name__ == '__main__': test()
