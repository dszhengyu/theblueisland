from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from pandas import DataFrame

pwd = 'z:\\theblueisland\\'
featureName = pwd + 'feature_label2\\feature_name.csv'

def extractFeature_Pandas(day, random = 1, target = 0, ratio = 32, 
                    prefix = pwd + "data_version2\\", 
                    prefix2 = pwd + "feature_label2\\"):
    if (target == 0):
        ufile = prefix + "u_" + day + ".csv"
        ifile = prefix + "i_" + day + ".csv"
        lfile = prefix + "l_" + day + ".csv"
        uptime = datetime.strptime('2014_' + day + ' 00:00:00', "%Y_%m_%d %H:%M:%S")
        uptime += timedelta(days = 9, hours = 23)
        if (random == 1):
            featureDay = prefix2 + "feature_" + day + ".csv"
            labelDay = prefix2 + "label_" + day + ".csv"
        else:
            featureDay = prefix2 + "test_feature_" + day + ".csv"
            labelDay = prefix2 + "test_label_" + day + ".csv"

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
    xTotalFeature = xTotalGroup['time'].count().unstack('behavior_type')
    xTotalFeature.sort_index(axis = 1, inplace = True)
    xTotalFeature = xTotalFeature.add_prefix('x_total_')
    xTotalFeature.fillna(value = 0, inplace = True)
    xTotalFeature13 = xTotalFeature.ix[:, ['x_total_1', 'x_total_3']]
    # x 4 div all
    xTotalFeature['x_4divall'] = xTotalFeature['x_total_4'] / xTotalFeature.sum(axis = 1)
    # 4 div 1
    xTotalFeature['x_4div1'] = xTotalFeature['x_total_4'].div(xTotalFeature['x_total_1'])
    xTotalFeature[xTotalFeature['x_4div1'] == np.inf] = 0
    #last intersect
    xLastTimeFeature = xTotalGroup['time'].min().unstack('behavior_type')
    xLastTimeFeature.fillna(value = 10, inplace = True)
    xLastTimeFeature.sort_index(axis = 1, inplace = True)
    xLastTimeFeature = xLastTimeFeature.add_prefix('x_last_time_')
    xLastTimeFeature13 = xLastTimeFeature.ix[ : , ['x_last_time_1', 'x_last_time_3']]
    #time relative
    xTimeGroup = u.groupby(['user_id', 'item_id', 'time', 'behavior_type'])
    xTimeFeature = xTimeGroup['item_category'].count()
    xTimeFeature = xTimeFeature.unstack(['time', 'behavior_type'])
    xTimeFeature.sort_index(axis = 1, inplace = True)
    xTimeFeature.fillna(value = 0, inplace = True)
    # 3 not 4
    x_last1_3not4 = DataFrame(index = xTimeFeature[0].index)
    x_last1_3not4_index = np.logical_and(xTimeFeature[0][4] == 0, xTimeFeature[0][3] != 0)
    x_last1_3not4.ix[x_last1_3not4_index, 'x_last1_3not4'] = 1
    x_last1_3not4.fillna(0, inplace = True)
    #last
    xlast1 = (xTimeFeature[0]).add_prefix('x_last_1')
    xlast3 = (xTimeFeature[0] + xTimeFeature[1] + xTimeFeature[2]).add_prefix('x_last_3')
    xlast5 = (xTimeFeature[0] + xTimeFeature[1] + xTimeFeature[2] 
                + xTimeFeature[3] + xTimeFeature[4]).add_prefix('x_last_5')
    # xT = pd.concat([xlast1, xlast3, xlast5], axis = 1)
    xlast1_13 = xlast1.ix[ : , ['x_last_11', 'x_last_13']]
    xlast3_13 = xlast3.ix[ : , ['x_last_31', 'x_last_33']]
    xlast5_13 = xlast5.ix[ : , ['x_last_51', 'x_last_53']]
    xT13 = pd.concat([xlast1_13, xlast3_13, xlast5_13], axis = 1)
    #sum up
    xfeature = pd.concat([xTotalFeature13, xLastTimeFeature13, 
                    xT13, xTotalFeature['x_4divall'], xTotalFeature['x_4div1'], 
                        x_last1_3not4], axis = 1)

## USER
   # total
    uTotalGroup = u.groupby(['user_id', 'behavior_type'])
    uTotalFeature = uTotalGroup['item_id'].count().unstack('behavior_type')
    uTotalFeature.sort_index(axis = 1, inplace = True)
    uTotalFeature = uTotalFeature.add_prefix('u_total_')
    uTotalFeature.fillna(0, inplace = True)
    # nunique()
    uTotalUnique = uTotalGroup['item_id'].nunique().unstack('behavior_type')
    uTotalUnique.sort_index(axis = 1, inplace = True)
    uTotalUnique = uTotalUnique.add_prefix('u_unique_')
    uTotalUnique.fillna(0, inplace = True)
    # item rate
    uTotalFeature['u_average_1'] = uTotalFeature['u_total_1'] / uTotalUnique['u_unique_1']
    uTotalFeature[uTotalFeature['u_average_1']  == np.inf] = 0
    uTotalFeature['u_average_3'] = uTotalFeature['u_total_3'] / uTotalUnique['u_unique_3']
    uTotalFeature[uTotalFeature['u_average_3']  == np.inf] = 0
    # 4 div 1
    uTotalFeature['u_4div1'] = uTotalFeature['u_total_4'].div(uTotalFeature['u_total_1'])
    uTotalFeature[uTotalFeature['u_4div1'] == np.inf] = 0
    # 4 div all
    uTotalFeature['u_4divall'] = uTotalFeature['u_total_4'] / uTotalFeature.sum(axis = 1)
    # 3 div 1
    uTotalFeature['u_3div1'] = uTotalFeature['u_total_3'].div(uTotalFeature['u_total_1'])
    uTotalFeature[uTotalFeature['u_3div1'] == np.inf] = 0
    # 3 div all
    uTotalFeature['u_3divall'] = uTotalFeature['u_total_3'] / uTotalFeature.sum(axis = 1)
    # 4 div 3
    uTotalFeature['u_4div3'] = uTotalFeature['u_total_4'].div(uTotalFeature['u_total_3'])
    uTotalFeature[uTotalFeature['u_4div3'] == np.inf] = 0
    uTotalFeature.fillna(0, inplace = True)
    #time relative
    uTimeGroup = u.groupby(['user_id', 'time', 'behavior_type'])
    uTimeFeature = uTimeGroup['item_category'].count()
    uTimeFeature = uTimeFeature.unstack(['time', 'behavior_type'])
    uTimeFeature.sort_index(axis = 1, inplace = True)
    uTimeFeature.fillna(value = 0, inplace = True)
    #last
    ulast1 = (uTimeFeature[0]).add_prefix('u_last_1')
    ulast3 = (uTimeFeature[0] + uTimeFeature[1] + uTimeFeature[2]).add_prefix('u_last_3')
    ulast5 = (uTimeFeature[0] + uTimeFeature[1] + uTimeFeature[2] 
                + uTimeFeature[3] + uTimeFeature[4]).add_prefix('u_last_5')
    uT = pd.concat([ulast1, ulast3, ulast5], axis = 1)
    # ulast 1
    ulast1_1 = ulast1['u_last_11']
    ulast3_1 = ulast3['u_last_31']
    ulast5_1 = ulast5['u_last_51']
    uT1 = pd.concat([ulast1_1, ulast3_1, ulast5_1], axis = 1)
    # u active days
    uSingleGroup = u.groupby(['user_id'])
    uActiveDays = uSingleGroup['time'].nunique()
    # u active in 1, 3, 5 days
    # TO-DO
    #sum up
    ufeature = pd.concat([uTotalFeature, uTotalUnique, uT1, uActiveDays], axis = 1)
## ITEM
    # total
    i = pd.read_csv(ifile, names = columns, parse_dates = [5])
    i['time'] = (uptime - i['time']).astype('timedelta64[D]')
    iTotalGroup = i.groupby(['item_id', 'behavior_type'])
    iTotalFeature = iTotalGroup['user_id'].count().unstack('behavior_type')
    iTotalFeature.sort_index(axis = 1, inplace = True)
    iTotalFeature = iTotalFeature.add_prefix('i_total_')
    iTotalFeature13 = iTotalFeature.ix[:, ['i_total_1', 'i_total_3']]
    # # i nunique()
    # iTotalUnique = iTotalGroup['user_id'].agg(lambda x: len(x.unique())).unstack('behavior_type')
    # iTotalUnique.sort_index(axis = 1, inplace = True)
    # iTotalUnique = iTotalUnique.add_prefix('i_unique_')
    # iTotalUnique.fillna(value = 0, inplace = True)
    #rate
    iTotalFeature['i_4divall'] = iTotalFeature['i_total_4'] / iTotalFeature.sum(axis = 1)
    #last intersect
    iLastTimeFeature = iTotalGroup['time'].min().unstack('behavior_type')
    iLastTimeFeature.sort_index(axis = 1, inplace = True)
    iLastTimeFeature = iLastTimeFeature.add_prefix('i_last_time_')
    iLastTimeFeature13 = iLastTimeFeature.ix[ : , ['i_last_time_1', 'i_last_time_3']]
    # time relative
    iTimeGroup = u.groupby(['item_id', 'time', 'behavior_type'])
    iTimeFeature = iTimeGroup['item_category'].count()
    iTimeFeature = iTimeFeature.unstack(['time', 'behavior_type'])
    iTimeFeature.sort_index(axis = 1, inplace = True)
    iTimeFeature.fillna(value = 0, inplace = True)
    #last
    ilast1 = (iTimeFeature[0]).add_prefix('i_last_1')
    ilast3 = (iTimeFeature[0] + iTimeFeature[1] + iTimeFeature[2]).add_prefix('i_last_3')
    ilast5 = (iTimeFeature[0] + iTimeFeature[1] + iTimeFeature[2] 
                + iTimeFeature[3] + iTimeFeature[4]).add_prefix('i_last_5')
    iT = pd.concat([ilast1, ilast3, ilast5], axis = 1)
    ilast1_1 = ilast1['i_last_11']
    ilast3_1 = ilast3['i_last_31']
    ilast5_1 = ilast5['i_last_51']
    iT1 = pd.concat([ilast1_1, ilast3_1, ilast5_1], axis = 1)
    #sum up
    ifeature = pd.concat([iTotalFeature13, iTotalFeature['i_4divall'], 
                            iLastTimeFeature13, iT1], axis = 1)
    
## COMBINE
    finalXy = pd.merge(xfeature, ifeature, how = 'left', 
                            left_index = True, right_index = True, sort = False)
    finalXy = pd.merge(finalXy, ufeature, how = 'left', 
                            left_index = True, right_index = True, sort = False)
    finalXy.fillna(0, inplace = True)
##LABEL & RANDOM
    #merge X and y
    if (not target):
        labels = pd.read_csv(lfile, names = columns[0 : 2], 
                                index_col = ['user_id', 'item_id'])
        labels['buy'] = 1
        finalXy = pd.merge(finalXy, labels, how = 'left', 
                                left_index = True, right_index = True, sort = False)  
        #random the zeros
        if (random):
            ones = finalXy[finalXy['buy'] ==1]
            zeros = finalXy[finalXy['buy'].isnull()]
            zerosCount = (ratio - 1) * len(ones)
            zeros = zeros.ix[np.random.permutation(zeros.index)[ : zerosCount]]
            finalXy = pd.concat([ones, zeros])
            finalXy = finalXy.ix[np.random.permutation(finalXy.index)]
        #random complete
        finalXy.reset_index(inplace = True)
        finalXy.ix[ :, -1].to_csv(labelDay, na_rep = '0', 
                                    index = False, header = False)
        finalXy.drop(['user_id', 'item_id', 'buy'], axis = 1, inplace = True)
    else:
        # save target example
        finalXy.reset_index(inplace = True)
        finalXy.ix[ :, : 2].to_csv(examplefilename, na_rep = '0', 
                                    index = False, header = False)
        finalXy.drop(['user_id', 'item_id'], axis = 1, inplace = True)
#done, write into file
    finalXy.to_csv(featureDay, na_rep = '0', index = False, header = False)
    finalXy[ : 0].to_csv(featureName, na_rep = '0', index = False, header = True)
##pandas end
    
    endTime = datetime.now()
    print (day, ' complete ', datetime.now())
    print (day , ' used time: ',  str(endTime - beginTime)) 
    print ('')

def test():
    extractFeature_Pandas('11_18')
    input('>>')

if __name__ == '__main__': test()
