#the split(",") func would return list like ['"abc"', '"..."', ..., '"..."\n']
#entry = [elm.strip('"\n') for elm in line.split(",")]

from datetime import datetime, timedelta

def extractFeature(day, prefix = "Z:\\theblueisland\\data_version2\\"):
    ufile = prefix + "u_" + day + ".csv"
    ifile = prefix + "i_" + day + ".csv"
    lfile = prefix + "l_" + day + ".csv"
    featureDay = prefix + "feature_" + day + ".csv"
    labelDay = prefix + "label_" + day + ".csv"
    uptime = datetime.strptime('2014_' + day + ' 00:00:00', "%Y_%m_%d %H:%M:%S")
    uptime += timedelta(days = 9, hours = 23)

    beginTime = datetime.now()
    
#load labelDict
    labelDict = {}
    l = open(lfile)
    for line in l.readlines():
        entry = [elm.strip('"\n') for elm in line.split(",")]
        labelDict[(entry[0], entry[1])] = None
    l.close()
        
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

#extract u-i & user feature, add item features
    features = []
    labels = []
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
            uiValue, label = selectFeatureLabel(userSet, uValue, itemDict, labelDict, uptime)
            features.extend(uiValue)
            labels.extend(label)
            userSet = []
            userSet.append(entry)
            curUser = entry[0]
    else:
        uValue = selectUserFeature(userSet, uptime)
        uiValue, label = selectFeatureLabel(userSet, uValue, itemDict, labelDict, uptime)
        features.extend(uiValue)
        labels.extend(label)
    f.close()

    endTime = datetime.now()
    print "used time: " + str(endTime - beginTime)
    input(">>")


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
    every1 = [routine[i][j] for i in range(10) for j in range (1, 5)]
    every2 = [routine[i][j] + routine[i + 1][j] for i in range(0, 10, 2) for j in range(1, 5)]
    every3 = [routine[i][j] + routine[i + 1][j] + routine[i + 2][j] for i in range(0, 9, 3) for j in range(1, 5)]
    totalPerson = 0
    total = [0, 0, 0, 0, 0]
    for key in person:
        total = [total[i] + person[key][i] for i in range(5)]
        totalPerson += 1
    return total[1 : 5] + [totalPerson] + every1 + every2 + every3
           

def selectUserFeature(userSet, uptime):
    'method to select user feature'
    #write into dict
    thing = {}
    for entry in userSet:
        behav = int(entry[2])
        thing.setdefault(entry[1], [0, 0, 0, 0, 0])
        thing[entry[1]][behav] += 1
    #sum uo the data in dict
    totalThing = 0
    total = [0, 0, 0, 0, 0]
    for key in thing:
        total = [total[i] + thing[key][i] for i in range(5)]
        totalThing += 1
    return total[1 : 5] + [totalThing]

def selectFeatureLabel(userSet, uValue, itemDict, labelDict, uptime):
    'method to select feature, based on <user_id, Item_id>'
    
    return [['uiValue']], [['label']]

def test():
    extractFeature('11_18');
    

if __name__ == '__main__': test()
