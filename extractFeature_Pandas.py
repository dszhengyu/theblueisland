from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from pandas import DataFrame

pwd = 'z:\\theblueisland\\'
day = '11_18'
target = 0
ratio = 10
prefix = pwd + "data_version2\\"
prefix2 = pwd + "feature_label\\"

def extractFeature_Pandas(day, random = 1, target = 0, ratio = 10, 
                    prefix = pwd + "data_version2\\", 
                    prefix2 = pwd + "feature_label\\"):
    if (target == 0):
        ufile = prefix + "u_" + day + ".csv"
        ifile = prefix + "i_" + day + ".csv"
        lfile = prefix + "l_" + day + ".csv"
        featureDay = prefix2 + "feature_" + day + ".csv"
        labelDay = prefix2 + "label_" + day + ".csv"
        uptime = datetime.strptime('2014_' + day + ' 00:00:00', 
                                    "%Y_%m_%d %H:%M:%S")
        uptime += timedelta(days = 9, hours = 23)
    else:
        ufile = prefix + "u_target.csv"
        ifile = prefix + "i_target.csv"
        featureDay = prefix2 + "feature_target.csv"
        examplefilename = prefix2 + "example_target.csv"
        uptime = datetime.strptime('2014_12_18 23:00:00', 
                                    "%Y_%m_%d %H:%M:%S")

    beginTime = datetime.now()
    print (beginTime)
    
##pandas on fire
    columns = ['user_id', 'item_id', 'behavior_type', 
                'user_geohash', 'item_category', 'time']
    i = pd.read_csv(ifile, names = columns)
    iTotalGroup = i.groupby(['item_id', 'behavior_type'])

    iTotalFeature = iTotalGroup['user_id'].count().unstack('behavior_type')
    iTotalFeature = iTotalFeature.add_prefix('item_total_')
    #item time relative feature to be complete
    
    #item
    
    u = pd.read_csv(ufile, names = columns)
    uTotalGroup = u.groupby(['user_id', 'behavior_type'])
    uTotalFeature = uTotalGroup['item_id'].count().unstack('behavior_type')
    uTotalFeature = uTotalFeature.add_prefix('user_total_')
    #user time relative
    
    #user
    
    xTotalGroup = u.groupby(['user_id', 'item_id', 'behavior_type'])
    xTotalFeature = xTotalGroup['item_category'].count().unstack('behavior_type')
    xTotalFeature = xTotalFeature.add_prefix('x_total_')
    #X time relative
    
    #X
    
    #merge X and y
    labels = pd.read_csv(lfile, names = columns[0 : 2], 
                            index_col = ['user_id', 'item_id'])
    labels['buy'] = 1
    
    finalXy = pd.merge(xTotalFeature, uTotalFeature, how = 'left', 
                            left_index = True, right_index = True, sort = False)
    finalXy = pd.merge(finalXy, iTotalFeature, how = 'left', 
                            left_index = True, right_index = True, sort = False)
    finalXy = pd.merge(finalXy, labels, how = 'left', 
                            left_index = True, right_index = True, sort = False)  
    finalXy.fillna(0)
    #merge complete
    
    #random the zeros
    if (not target and random):
        finalXy.reset_index(inplace = True)
        finalXy.drop(['user_id', 'item_id'], axis = 1, inplace = True)
        ones = finalXy[finalXy['buy'] ==1]
        zeros = finalXy[finalXy['buy'].isnull()]
        zerosCount = (ratio - 1) * len(ones)
        zeros = zeros.ix[np.random.permutation(zeros.index)[ : zerosCount]]
        finalXy = pd.concat([ones, zeros])
    #random complete
    
    #done, write into file
    finalXy.ix[ :, : -1].to_csv(featureDay, na_rep = '0', index = False, header = False)
    finalXy.ix[ :, -1].to_csv(labelDay, na_rep = '0', index = False, header = False)
    
    

##pandas end
    endTime = datetime.now()
    print (day, ' complete ' , datetime.now())
    print ("used time: " + str(endTime - beginTime)) 


def test():
    extractFeature_Pandas('12_8', 0)
    input('>>')

if __name__ == '__main__': test()
