from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from pandas import DataFrame

pwd = 'z:\\theblueisland\\'
day = '11_18'
target = 0
ratio = 10
prefix = pwd + "data_version2\\"
prefix2 = pwd + "feature_label2\\"

def extractFeature_Pandas(day, random = 1, target = 0, ratio = 7, 
                    prefix = pwd + "data_version2\\", 
                    prefix2 = pwd + "feature_label2\\"):
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
    print (day, ' start ', beginTime)
    
##pandas on fire
    columns = ['user_id', 'item_id', 'behavior_type', 
                'user_geohash', 'item_category', 'time']
## X
    #X, total
    u = pd.read_csv(ufile, names = columns, parse_dates = [5])
    u['time'] = (uptime - u['time']).astype('timedelta64[D]')
    xTotalGroup = u.groupby(['user_id', 'item_id', 'behavior_type'])
    xTotalFeature = xTotalGroup['item_category'].count().unstack('behavior_type')
    xTotalFeature = xTotalFeature.add_prefix('x_total_')
    #time relative
    xTimeGroup = u.groupby(['user_id', 'item_id', 'time', 'behavior_type'])
    xTimeFeature = xTimeGroup['item_category'].count()
    xTimeFeature = xTimeFeature.unstack(['time', 'behavior_type'])
    xTimeFeature.sort_index(axis = 1, inplace = True)
    xTimeFeature.fillna(value = 0, inplace = True)
    xlast1 = xTimeFeature[0]
    xlast3 = xTimeFeature[0] + xTimeFeature[1] + xTimeFeature[2]
    xlast5 = xlast3 + xTimeFeature[3] + xTimeFeature[4]
    xT = pd.concat([xlast1, xlast3, xlast5], axis = 1)
    xTotalFeature = pd.concat([xTotalFeature, xT], axis = 1)
##LABEL & RANDOM
    #merge X and y
    if (not target):
        labels = pd.read_csv(lfile, names = columns[0 : 2], 
                                index_col = ['user_id', 'item_id'])
        labels['buy'] = 1
        xTotalFeature = pd.merge(xTotalFeature, labels, how = 'left', 
                                left_index = True, right_index = True, sort = False)  
        
        #random the zeros
        if (random):
            ones = xTotalFeature[xTotalFeature['buy'] ==1]
            zeros = xTotalFeature[xTotalFeature['buy'].isnull()]
            zerosCount = (ratio - 1) * len(ones)
            zeros = zeros.ix[np.random.permutation(zeros.index)[ : zerosCount]]
            xTotalFeature = pd.concat([ones, zeros])
        #random complete
        xTotalFeature.ix[ :, -1].to_csv(labelDay, na_rep = '0', 
                                        index = False, header = False)
        xTotalFeature.drop('buy', axis = 1, inplace = True)
    else:
        # save target example
        example = DataFrame(index = xTotalFeature.index).reset_index()
        example.to_csv(examplefilename, na_rep = '0', index = False, header = False)

## USER
    # total
    uTotalGroup = u.groupby(['user_id', 'behavior_type'])
    uTotalFeature = uTotalGroup['item_id'].count().unstack('behavior_type')
    uTotalFeature = uTotalFeature.add_prefix('user_total_')
    #time relative
    uTimeGroup = u.groupby(['user_id', 'time', 'behavior_type'])
    uTimeFeature = uTimeGroup['item_category'].count()
    uTimeFeature = uTimeFeature.unstack(['time', 'behavior_type'])
    uTimeFeature.sort_index(axis = 1, inplace = True)
    uTimeFeature.fillna(value = 0, inplace = True)
    ulast1 = uTimeFeature[0]
    ulast3 = uTimeFeature[0] + uTimeFeature[1] + uTimeFeature[2]
    ulast5 = ulast3 + uTimeFeature[3] + uTimeFeature[4]
    uT = pd.concat([ulast1, ulast3, ulast5], axis = 1)
    uTotalFeature = pd.concat([uTotalFeature, uT], axis = 1)
## ITEM
    # total
    i = pd.read_csv(ifile, names = columns, parse_dates = [5])
    i['time'] = (uptime - i['time']).astype('timedelta64[D]')
    iTotalGroup = i.groupby(['item_id', 'behavior_type'])
    iTotalFeature = iTotalGroup['user_id'].count().unstack('behavior_type')
    iTotalFeature = iTotalFeature.add_prefix('item_total_')
    # time relative
    iTimeGroup = u.groupby(['item_id', 'time', 'behavior_type'])
    iTimeFeature = iTimeGroup['item_category'].count()
    iTimeFeature = iTimeFeature.unstack(['time', 'behavior_type'])
    iTimeFeature.sort_index(axis = 1, inplace = True)
    iTimeFeature.fillna(value = 0, inplace = True)
    ilast1 = iTimeFeature[0]
    ilast3 = iTimeFeature[0] + iTimeFeature[1] + iTimeFeature[2]
    ilast5 = ilast3 + iTimeFeature[3] + iTimeFeature[4]
    iT = pd.concat([ilast1, ilast3, ilast5], axis = 1)
    iTotalFeature = pd.concat([iTotalFeature, iT], axis = 1)
    
## COMBINE
    
    finalXy = pd.merge(xTotalFeature, uTotalFeature, how = 'left', 
                            left_index = True, right_index = True, sort = False)
    finalXy = pd.merge(finalXy, iTotalFeature, how = 'left', 
                            left_index = True, right_index = True, sort = False)
    finalXy.fillna(0, inplace = True)
    #done, write into file
    finalXy.to_csv(featureDay, na_rep = '0', index = False, header = False)
##pandas end
    
    endTime = datetime.now()
    print (day, ' complete ', datetime.now())
    print (day , ' used time: ',  str(endTime - beginTime)) 
    print ('')

def test():
    extractFeature_Pandas('11_18', 1)
    input('>>')

if __name__ == '__main__': test()
