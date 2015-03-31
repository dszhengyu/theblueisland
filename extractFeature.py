#the split(",") func would return list like ['"abc"', '"..."', ..., '"..."\n']
#to use the value as key or sth, you should call .strip('"') and
#for the last element in list, call .strip('"\n"')

from datetime import datetime

def extractFeature(day, prefix = "data_version2\\"):
    ufile = prefix + "u_" + day + ".csv"
    ifile = prefix + "i_" + day + ".csv"
    lfile = prefix + "l_" + day + ".csv"
    featureDay = prefix + "feature_" + day + ".csv"
    labelDay = prefix + "label_" + day + ".csv"

    beginTime = datetime.now()

    #d = datetime.strptime(x[5].strip("'\n"), '"%Y-%m-%d %H:%M:%S"')

#load labelDict
    labelDict = {}
    l = open(lfile)
    for line in l.readlines():
        entry = line.split(",")
        userL = entry[0].strip('"')
        itemL = entry[1].strip('"\n')
        labelDict[(userL, itemL)] = None
    l.close()

#extract item feature & put into itemDict
    itemDict = {}
    i = open(ifile)
    line = i.readline()
    curItem = line.split(",")[1]
    itemSet = []
    itemSet.append(line.split(","))
    for line in i.readlines():
        entry = line.split(",")
        if (entry[1] == curItem):
            itemSet.append(entry)
        else:
            iValue = selectItemFeature(itemSet)
            itemDict[curItem.strip('"')] = iValue
            itemSet = []
            itemSet.append(entry)
            curItem = entry[1]
    else:
        iValue = selectItemFeature(itemSet)
        itemDict[curItem.strip('"')] = iValue
    i.close()

#extract u-i & user feature, add item features
    features = []
    labels = []
    f = open(ufile)
    line = f.readline()
    curUser = line.split(",")[0]
    userSet = []
    userSet.append(line.split(","))
    for line in f.readlines():
        entry = line.split(",")
        if (entry[0] == curUser):
            userSet.append(entry)
        else:
            uValue = selectUserFeature(userSet)
            uiValue, label = selectFeatureLabel(userSet, uValue, itemDict, labelDict)
            features.extend(uiValue)
            labels.extend(label)
            userSet = []
            userSet.append(entry)
            curUser = entry[0]
    else:
        uValue = selectUserFeature(userSet)
        uiValue, label = selectFeatureLabel(userSet, uValue, itemDict, labelDict)
        features.extend(uiValue)
        labels.extend(label)
    f.close()

    endTime = datetime.now()
    print "used time: " + str(endTime - beginTime)

def selectItemFeature(itemSet):
    'method to select item feature'
    return []

def selectUserFeature(userSet):
    'method to select user feature'
    return []

def selectFeatureLabel(userSet, uValue, itemDict, labelDict):
    'method to select feature, based on <user_id, Item_id>'
    return [['uiValue']], [['label']]

def test():
    extractFeature("11_18");
    

if __name__ == '__main__': test()
