#the split(",") func would return list like ['"abc"', '"..."', ..., '"..."\n']
#entry = [elm.strip('"\n') for elm in line.split(",")]

from datetime import datetime, timedelta
from random import randint
import numpy as np

def extractFeature(day, target = 0, ratio = 4, prefix = "data_version2\\", prefix2 = "feature_label\\"):
    if (target == 0):
        ufile = prefix + "u_" + day + ".csv"
        ifile = prefix + "i_" + day + ".csv"
        lfile = prefix + "l_" + day + ".csv"
        featureDay = prefix2 + "feature_" + day + ".csv"
        labelDay = prefix2 + "label_" + day + ".csv"
        uptime = datetime.strptime('2014_' + day + ' 00:00:00', "%Y_%m_%d %H:%M:%S")
        uptime += timedelta(days = 9, hours = 23)
    else:
        ufile = prefix + "u_target.csv"
        ifile = prefix + "i_target.csv"
        featureDay = prefix2 + "feature_target.csv"
        examplefilename = prefix2 + "example_target.csv"
        uptime = datetime.strptime('2014_12_18 23:00:00', "%Y_%m_%d %H:%M:%S")

    beginTime = datetime.now()
    print (beginTime)
    
#load labelDict
    if (target == 0):
        labelDict = {}
        l = open(lfile)
        for line in l.readlines():
            entry = [elm.strip('"\n') for elm in line.split(",")]
            labelDict[(entry[0], entry[1])] = None
        l.close()
    else:
        labelDict = {}

    print (day, ' labelDict complete, ', datetime.now())
        
#extract item feature & put into itemDict
    itemDict = {}
    i = open(ifile)
    line = i.readline()
    entry = [elm.strip('"\n') for elm in line.split(",")]
    curItem = entry[1]
    itemSet = []
    itemSet.append(entry)
    for line in i.readlines():
        entry = [elm.strip('"\n') for elm in line.split(",")]
        if (entry[1] == curItem):
            itemSet.append(entry)
        else:
            iValue = selectItemFeature(itemSet, uptime)
            itemDict[curItem] = iValue
            itemSet = []
            itemSet.append(entry)
            curItem = entry[1]
    else:
        iValue = selectItemFeature(itemSet, uptime)
        itemDict[curItem] = iValue
    i.close()
    
    print (day, ' itemDict complete, ' , datetime.now())

#extract u-i & user feature, add item features
    if (target == 0):
        randRange = 3500000 / (1000 * ratio)
    else:
        randRange = 0
    features = []
    labels = []
    examples = []
    f = open(ufile)
    line = f.readline()
    entry = [elm.strip('"\n') for elm in line.split(",")]
    curUser = entry[0]
    userSet = []
    userSet.append(entry)
    for line in f.readlines():
        entry = [elm.strip('"\n') for elm in line.split(",")]
        if (entry[0] == curUser):
            userSet.append(entry)
        else:
            uValue = selectUserFeature(userSet, uptime)
            uiValue, label, example = selectFeatureLabel(userSet, uValue, itemDict, labelDict, uptime, randRange)
            features.extend(uiValue)
            labels.extend(label)
            examples.extend(example)
            userSet = []
            userSet.append(entry)
            curUser = entry[0]
    else:
        uValue = selectUserFeature(userSet, uptime)
        uiValue, label, example= selectFeatureLabel(userSet, uValue, itemDict, labelDict, uptime, randRange)
        features.extend(uiValue)
        labels.extend(label)
        examples.extend(example)
    f.close()

    print (day, ' features extraction complete, start writing... ', datetime.now())

#write into files

    featurefile = open(featureDay, "w")
    for line in features:
        tmp = ','.join([str(i) for i in line]) + '\n'
        featurefile.write(tmp)
    featurefile.close()
    
    if (target == 0):
        labelfile = open(labelDay, "w")
        for line in labels:
            tmp = ','.join([str(i) for i in line]) + '\n'
            labelfile.write(tmp)
        labelfile.close()
    else:
        examplefile = open(examplefilename, "w")
        for line in examples:
            tmp = ','.join([str(i) for i in line]) + '\n'
            examplefile.write(tmp)
        examplefile.close()
         
    endTime = datetime.now()
    print (day, ' complete ' , datetime.now())
    print ("used time: " + str(endTime - beginTime)) 

def selectItemFeature(itemSet, uptime):
    'method to select item feature'
    #write into table and dict
    routine = [[0 for _ in range(5)] for _ in range(10)]
    person = {}
    for entry in itemSet:
        deltaDay = (uptime - datetime.strptime(entry[5], "%Y-%m-%d %H:%M:%S")).days
        behav = int(entry[2])
        routine[deltaDay][behav] += 1
        person.setdefault(entry[0], [0, 0, 0, 0, 0])
        person[entry[0]][behav] += 1
    #sum up the data in routine and dict
#    every1 = [routine[i][j] for i in range(10) for j in range (1, 5)]
    every2 = [routine[i][j] + routine[i + 1][j] for i in range(0, 10, 2) for j in range(1, 5)]
#    every3 = [routine[i][j] + routine[i + 1][j] + routine[i + 2][j] for i in range(0, 9, 3) for j in range(1, 5)]
    totalPerson = 0
    total = [0, 0, 0, 0, 0]
    for key in person:
        total = [total[i] + person[key][i] for i in range(5)]
        totalPerson += 1
    return total[1 : 5] + every2
           

def selectUserFeature(userSet, uptime):
    'method to select user feature'
    #write into dict
    thing = {}
    for entry in userSet:
        behav = int(entry[2])
        thing.setdefault(entry[1], [0, 0, 0, 0, 0])
        thing[entry[1]][behav] += 1
    #sum up the data in dict
    totalThing = 0
    total = [0, 0, 0, 0, 0]
    for key in thing:
        total = [total[i] + thing[key][i] for i in range(5)]
        totalThing += 1
    return []

def selectFeatureLabel(userSet, uValue, itemDict, labelDict, uptime, randRange):
    'method to select feature, based on <user_id, Item_id>'
    features = []
    labels = []
    examples = []
    curItem = userSet[0][1]
    curUser= userSet[0][0]
    uiSet = []
    uiSet.append(userSet[0])
    for entry in userSet[1 :]:
        if (entry[1] == curItem):
            uiSet.append(entry)
        else:
            if ((curUser, curItem) in labelDict):
                label = 1
            elif(randint(0, randRange) == 0):
                label = 0
            else:
                uiSet = []
                uiSet.append(entry)
                curItem = entry[1]
                continue
            singleUIValue = selectSingleFeature(uiSet, uptime)
            iValue = itemDict.get(curItem, [])
            example = [curUser, curItem]
            features.append(singleUIValue + uValue + iValue)
            labels.append([label])
            examples.append(example)         
            uiSet = []
            uiSet.append(entry)
            curItem = entry[1]
    else:
        if ((curUser, curItem) in labelDict):
            label = 1
        elif(randint(0, randRange) == 0):
            label = 0
        else:
            return features, labels, examples
        singleUIValue = selectSingleFeature(uiSet, uptime)
        iValue = itemDict.get(curItem, [])
        example = [curUser, curItem]
        features.append(singleUIValue + uValue + iValue)
        labels.append([label])
        examples.append(example)
    return features, labels, examples
    
def selectSingleFeature(uiSet, uptime):
    'return ui-feature'
    #write into table and total_behav
    routine = [[0 for _ in range(5)] for _ in range(10)]
    total = [0, 0, 0, 0, 0]
    for entry in uiSet:
        deltaDay = (uptime - datetime.strptime(entry[5], "%Y-%m-%d %H:%M:%S")).days
        behav = int(entry[2])
        routine[deltaDay][behav] += 1
        total[behav] += 1
    #sum up the data in routine
#    every1 = [routine[i][j] for i in range(10) for j in range (1, 5)]
    every2 = [routine[i][j] + routine[i + 1][j] for i in range(0, 10, 2) for j in range(1, 5)]
#    every3 = [routine[i][j] + routine[i + 1][j] + routine[i + 2][j] for i in range(0, 9, 3) for j in range(1, 5)]
    return total[1 : 5] + every2

def unitTest4_selectFeatureLabel():
    userSet = [['121', '3232', '1', 'qwq', '1212', '2014-11-19 20:00:00'],
             ['121', '3232', '3', 'qwq', '1212', '2014-11-19 20:00:00'],
             ['121', '3232', '1', 'qwq', '1212', '2014-11-19 20:00:00'],
             ['121', '3232', '1', 'qwq', '1212', '2014-11-19 20:00:00'],
             ['121', '3232', '4', 'qwq', '1212', '2014-11-19 5:00:00'],
             ['121', '3232', '1', 'qwq', '1212', '2014-11-19 10:00:00'],
               ['121', '32', '1', 'qwq', '1212', '2014-11-19 10:00:00'],
               ['121', '32', '1', 'qwq', '1212', '2014-11-19 10:00:00'],
               ['121', '3111', '1', 'qwq', '1212', '2014-11-19 10:00:00'],
               ['121', '322212', '1', 'qwq', '1212', '2014-11-19 10:00:00']]
    
    uiSet = [['121', '3232', '1', 'qwq', '1212', '2014-11-19 20:00:00'],
             ['121', '3232', '3', 'qwq', '1212', '2014-11-19 20:00:00'],
             ['121', '3232', '1', 'qwq', '1212', '2014-11-19 20:00:00'],
             ['121', '3232', '1', 'qwq', '1212', '2014-11-19 20:00:00'],
             ['121', '3232', '4', 'qwq', '1212', '2014-11-19 5:00:00'],
             ['121', '3232', '1', 'qwq', '1212', '2014-11-19 10:00:00']]
    
    uptime = datetime.strptime('2014_11_28 23:00:00', "%Y_%m_%d %H:%M:%S")
    uValue = [199,99,99,99]
    itemDict = {'3232': [88, 88, 88], '3111': [88888, 88888]}
    labelDict = {('121', '3232'): None}
    
    x, y, z = selectFeatureLabel(userSet, uValue, itemDict, labelDict, uptime, 5)
    
    print (x, len(x))
    print (y, len(y))
    print (z, len(z))
    
    input('>>')

def test():
    extractFeature('11_18', 0)
    input('>>')

if __name__ == '__main__': test()
