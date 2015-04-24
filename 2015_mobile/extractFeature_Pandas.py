from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.cluster import KMeans

pwd = 'z:\\theblueisland\\'
featureName = pwd + 'feature_label2\\feature_name.csv'
test = 1
target = 0
ratio = 40
prefix = pwd + "data_version2\\"
prefix2 = pwd + "feature_label2\\"
day = '12_8'

def extractFeature_Pandas(day, test = 0, target = 0, ratio = 40, 
                    prefix = pwd + "data_version2\\", 
                    prefix2 = pwd + "feature_label2\\"):
    if (target == 0):
        ufile = prefix + "u_" + day + ".csv"
        ifile = prefix + "i_" + day + ".csv"
        lfile = prefix + "l_" + day + ".csv"
        uptime = datetime.strptime('2014_' + day + ' 00:00:00', "%Y_%m_%d %H:%M:%S")
        uptime += timedelta(days = 9, hours = 23)
        if (test == 0):
            featureDay = prefix2 + "feature_" + day + ".csv"
            labelDay = prefix2 + "label_" + day + ".csv"
            exampleDay = prefix2 + "example_" + day + ".csv"
            itemFeature = prefix2 + "item_feature" + day + ".csv"
            itemLabel = prefix2 + "item_label" + day + ".csv"
        else:
            featureDay = prefix2 + "test_feature_" + day + ".csv"
            labelDay = prefix2 + "test_label_" + day + ".csv"
            exampleDay = prefix2 + "test_example_" + day + ".csv"
            itemFeature = prefix2 + "test_item_feature" + day + ".csv"
            itemLabel = prefix2 + "test_item_label" + day + ".csv"
    else:
        ufile = prefix + "u_target.csv"
        ifile = prefix + "i_target.csv"
        featureDay = prefix2 + "feature_target.csv"
        itemFeature = prefix2 + "item_feature_target" + day + ".csv"
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
    u['time'] = uptime - u['time']
    u['timeD'] = u['time'].astype('timedelta64[D]')
    xTotalGroup = u.groupby(['user_id', 'item_id', 'behavior_type'])
    xTotalFeature = xTotalGroup['timeD'].count().unstack('behavior_type')
    xTotalFeature.sort_index(axis = 1, inplace = True)
    xTotalFeature = xTotalFeature.add_prefix('x_total_')
    xTotalFeature.fillna(value = 0, inplace = True)
    xTotalFeature13 = xTotalFeature.ix[:, ['x_total_1', 'x_total_3']]
    # x 4 div all
    xTotalFeature['x_4divall'] = xTotalFeature['x_total_4'] / xTotalFeature.sum(axis = 1)
    # 4 div 1
    xTotalFeature['x_4div1'] = xTotalFeature['x_total_4'].div(xTotalFeature['x_total_1'])
    xTotalFeature[xTotalFeature['x_4div1'] == np.inf] = 0
    # 3 div 1
    xTotalFeature['x_3div1'] = xTotalFeature['x_total_3'].div(xTotalFeature['x_total_1'])
    xTotalFeature[xTotalFeature['x_3div1'] == np.inf] = 0
    # 3 div all
    xTotalFeature['x_3divall'] = xTotalFeature['x_total_3'] / xTotalFeature.sum(axis = 1)
    #last intersect
    xLastTimeFeature = xTotalGroup['timeD'].min().unstack('behavior_type')
    xLastTimeFeature.fillna(value = 10, inplace = True)
    xLastTimeFeature.sort_index(axis = 1, inplace = True)
    xLastTimeFeature = xLastTimeFeature.add_prefix('x_last_time_')
    xLastTimeFeature13 = xLastTimeFeature.ix[ : , ['x_last_time_1', 'x_last_time_3']]
    #timeD relative
    xTimeGroup = u.groupby(['user_id', 'item_id', 'timeD', 'behavior_type'])
    xTimeFeature = xTimeGroup['item_category'].count()
    xTimeFeature = xTimeFeature.unstack(['timeD', 'behavior_type'])
    xTimeFeature.sort_index(axis = 1, inplace = True)
    xTimeFeature.fillna(value = 0, inplace = True)
    # last1 3 not 4
    x_last1_3not4 = DataFrame(index = xTimeFeature[0].index)
    x_last1_3not4_index = np.logical_and(xTimeFeature[0][4] == 0, xTimeFeature[0][3] != 0)
    x_last1_3not4.ix[x_last1_3not4_index, 'x_last1_3not4'] = 1
    x_last1_3not4.fillna(0, inplace = True)
    # last2 3 ont 4
    x_last2_3not4 = DataFrame(index = xTimeFeature[0].index)
    x_last2_3not4_index = np.logical_and(xTimeFeature[1][4] == 0, xTimeFeature[1][3] != 0)
    x_last2_3not4_index = np.logical_and(x_last2_3not4_index, xTimeFeature[0][4] == 0)
    x_last2_3not4_index = np.logical_or(x_last2_3not4_index, x_last1_3not4_index)
    x_last2_3not4.ix[x_last2_3not4_index, 'x_last2_3not4'] = 1
    x_last2_3not4.fillna(0, inplace = True)
    # last3 3 not 4
    x_last3_3not4 = DataFrame(index = xTimeFeature[0].index)
    x_last3_3not4_index = np.logical_and(xTimeFeature[2][4] == 0, xTimeFeature[2][3] != 0)
    x_last3_3not4_index = np.logical_and(x_last3_3not4_index, xTimeFeature[1][4] == 0)
    x_last3_3not4_index = np.logical_and(x_last3_3not4_index, xTimeFeature[0][4] == 0)
    x_last3_3not4_index = np.logical_or(x_last3_3not4_index, x_last1_3not4_index)
    x_last3_3not4_index = np.logical_or(x_last3_3not4_index, x_last2_3not4_index)
    x_last3_3not4.ix[x_last3_3not4_index, 'x_last3_3not4'] = 1
    x_last3_3not4.fillna(0, inplace = True)
    #last
    xlast1 = (xTimeFeature[0]).add_prefix('x_last_1')
    xlast2 = (xTimeFeature[0] + xTimeFeature[1]).add_prefix('x_last_2')
    xlast3 = (xTimeFeature[0] + xTimeFeature[1] + xTimeFeature[2]).add_prefix('x_last_3')
    xlast4 = (xTimeFeature[0] + xTimeFeature[1] + xTimeFeature[2] 
                + xTimeFeature[3]).add_prefix('x_last_4')
    xlast5 = (xTimeFeature[0] + xTimeFeature[1] + xTimeFeature[2] 
                + xTimeFeature[3] + xTimeFeature[4]).add_prefix('x_last_5')
    xT = pd.concat([xlast1, xlast3, xlast5], axis = 1)
    xlast1_13 = xlast1.ix[ : , ['x_last_11']]
    xlast2_13 = xlast2.ix[ : , ['x_last_21']]
    xlast3_13 = xlast3.ix[ : , ['x_last_31']]
    xlast4_13 = xlast4.ix[ : , ['x_last_41', 'x_last_43']]
    xlast5_13 = xlast5.ix[ : , ['x_last_51', 'x_last_53']]
    xT13 = pd.concat([xlast1_13, xlast2_13, xlast3_13, xlast5_13], axis = 1)
    #sum up
    xfeature = pd.concat([xTotalFeature13, xLastTimeFeature13, xT13, 
                        xTotalFeature['x_4divall'], xTotalFeature['x_4div1'], 
                        x_last1_3not4, x_last2_3not4, x_last3_3not4], axis = 1)
## USER
    # total
    uTotalGroup = u.groupby(['user_id', 'behavior_type'])
    uTotalFeature = uTotalGroup['item_id'].count().unstack('behavior_type')
    uTotalFeature.sort_index(axis = 1, inplace = True)
    uTotalFeature = uTotalFeature.add_prefix('u_total_')
    uTotalFeature.fillna(0, inplace = True)
    uTotalFeature134 = uTotalFeature.ix[ : , ['u_total_1', 'u_total_3', 'u_total_4']]
    # nunique()
    uTotalUnique = uTotalGroup['item_id'].nunique().unstack('behavior_type')
    uTotalUnique.sort_index(axis = 1, inplace = True)
    uTotalUnique = uTotalUnique.add_prefix('u_unique_')
    uTotalUnique.fillna(0, inplace = True)
    uTotalUnique14 = uTotalUnique.ix[ :, ['u_unique_1', 'u_unique_4']]
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
    #timeD relative
    uTimeGroup = u.groupby(['user_id', 'timeD', 'behavior_type'])
    uTimeFeature = uTimeGroup['item_category'].count()
    uTimeFeature = uTimeFeature.unstack(['timeD', 'behavior_type'])
    uTimeFeature.sort_index(axis = 1, inplace = True)
    uTimeFeature.fillna(value = 0, inplace = True)
    # #last
    ulast1 = (uTimeFeature[0]).add_prefix('u_last_1')
    ulast2 = (uTimeFeature[0] + uTimeFeature[1]).add_prefix('u_last_2')
    ulast3 = (uTimeFeature[0] + uTimeFeature[1] + uTimeFeature[2]).add_prefix('u_last_3')
    ulast4 = (uTimeFeature[0] + uTimeFeature[1] + uTimeFeature[2] 
                + uTimeFeature[3]).add_prefix('u_last_4')
    ulast5 = (uTimeFeature[0] + uTimeFeature[1] + uTimeFeature[2] 
                + uTimeFeature[3] + uTimeFeature[4]).add_prefix('u_last_5')
    uT = pd.concat([ulast1, ulast2, ulast3, ulast4, ulast5], axis = 1)
    ulast1_3 = ulast1['u_last_13']
    ulast2_3 = ulast2['u_last_23']
    ulast3_13 = ulast3.ix[ : , ['u_last_31', 'u_last_33']]
    ulast4_134 = ulast4.ix[ : , ['u_last_41', 'u_last_43', 'u_last_44']]
    ulast5_134 = ulast5.ix[ : , ['u_last_51', 'u_last_53', 'u_last_54']]
    uT134 = pd.concat([ulast1_3, ulast3_13, ulast5_134], axis = 1)
    #sum up
    ufeature = pd.concat([uTotalFeature134, uTotalUnique14, uT134], axis = 1)
## ITEM
    # total
    i = pd.read_csv(ifile, names = columns, parse_dates = [5])
    i['time'] = uptime - i['time']
    i['timeD'] = i['time'].astype('timedelta64[D]')
    iTotalGroup = i.groupby(['item_id', 'behavior_type'])
    iTotalFeature = iTotalGroup['user_id'].count().unstack('behavior_type')
    iTotalFeature.sort_index(axis = 1, inplace = True)
    iTotalFeature = iTotalFeature.add_prefix('i_total_')
    iTotalFeature4 = iTotalFeature.ix[ : , 'i_total_4']
    # 3 div 1
    iTotalFeature['i_3div1'] = iTotalFeature['i_total_3'].div(iTotalFeature['i_total_1'])
    iTotalFeature[iTotalFeature['i_3div1'] == np.inf] = 0
    # 4 div 1
    iTotalFeature['i_4div1'] = iTotalFeature['i_total_4'].div(iTotalFeature['i_total_1'])
    iTotalFeature[iTotalFeature['i_4div1'] == np.inf] = 0
    # 4 div all
    iTotalFeature['i_4divall'] = iTotalFeature['i_total_4'] / iTotalFeature.sum(axis = 1)
    # 3 div all
    iTotalFeature['i_3divall'] = iTotalFeature['i_total_3'] / iTotalFeature.sum(axis = 1)
    # timeD relative
    iTimeGroup = i.groupby(['item_id', 'timeD', 'behavior_type'])
    iTimeFeature = iTimeGroup['item_category'].count()
    iTimeFeature = iTimeFeature.unstack(['timeD', 'behavior_type'])
    iTimeFeature.sort_index(axis = 1, inplace = True)
    iTimeFeature.fillna(value = 0, inplace = True)
    #last
    ilast1 = (iTimeFeature[0]).add_prefix('i_last_1')
    ilast2 = (iTimeFeature[0] + iTimeFeature[1]).add_prefix('i_last_2')
    ilast3 = (iTimeFeature[0] + iTimeFeature[1] + iTimeFeature[2]).add_prefix('i_last_3')
    ilast4 = (iTimeFeature[0] + iTimeFeature[1] + iTimeFeature[2] 
                + iTimeFeature[3]).add_prefix('i_last_4')
    ilast5 = (iTimeFeature[0] + iTimeFeature[1] + iTimeFeature[2] 
                + iTimeFeature[3] + iTimeFeature[4]).add_prefix('i_last_5')
    iT = pd.concat([ilast1, ilast2, ilast3, ilast4, ilast5], axis = 1)
    ilast1_13 = ilast1.ix[:, ['i_last_11', 'i_last_13']]
    ilast3_13 = ilast3.ix[:, ['i_last_31', 'i_last_33']]
    ilast5_13 = ilast3.ix[:, ['i_last_51', 'i_last_53']]
    iT13 = pd.concat([ilast1_13, ilast3_13, ilast5_13], axis = 1)
    #sum up
    ifeature = pd.concat([iTotalFeature4, iTotalFeature['i_4divall'], 
                        iTotalFeature['i_3div1'], iTotalFeature['i_4div1'], 
                        iTotalFeature['i_3divall'], iT13], axis = 1)
    ifeature2 = pd.concat([iTotalFeature4, iTotalFeature['i_4divall'], 
                        iTotalFeature['i_3div1'], iTotalFeature['i_4div1'], 
                        iTotalFeature['i_3divall'], iT13], axis = 1)
    
    #category
    categoryGroup = i.groupby(['item_category', 'behavior_type'])
    categoryTotal = categoryGroup['time'].count().unstack('behavior_type')
    categoryTotal = categoryTotal.add_prefix('c_total_')
    categoryTotal.fillna(0, inplace = True)
    categoryTotal = categoryTotal.reset_index('item_category')
    categoryItemGroup = i.groupby(['item_category', 'item_id', 'behavior_type'])
    categoryItemTotal = categoryItemGroup['time'].count().unstack('behavior_type')
    categoryItemTotal = categoryItemTotal.add_prefix('c_i_total_')
    categoryItemTotal.fillna(0, inplace = True)
    categoryItemTotal = categoryItemTotal.reset_index()
    categoryFeature = pd.merge(categoryItemTotal, categoryTotal, 
                                left_on = 'item_category', right_on = 'item_category',)
    categoryFeature.drop('item_category', inplace = True, axis = 1)
    categoryFeature.set_index('item_id', inplace = True)
    categoryFeature['c_i_rate_1'] = categoryFeature['c_i_total_1'] / categoryFeature['c_total_1']
    categoryFeature['c_i_rate_2'] = categoryFeature['c_i_total_2'] / categoryFeature['c_total_2']
    categoryFeature['c_i_rate_3'] = categoryFeature['c_i_total_3'] / categoryFeature['c_total_3']
    categoryFeature['c_i_rate_4'] = categoryFeature['c_i_total_4'] / categoryFeature['c_total_4']
    
    categoryFeature['c_i_rate_1'] *= categoryFeature['c_total_4']
    categoryFeature['c_i_rate_2'] *= categoryFeature['c_total_4']
    categoryFeature['c_i_rate_3'] *= categoryFeature['c_total_4']
    categoryFeature['c_i_rate_4'] *= categoryFeature['c_total_4']
    
    categoryFeatureRate = categoryFeature.ix[ : , 'c_i_rate_1' : 'c_i_rate_4']
    categoryFeatureRate.fillna(0, inplace = True)
    #category done
    ifeature = pd.merge(ifeature, categoryFeatureRate, 
                        left_index = True, right_index = True, sort = False)
                        
    ifeature2 = pd.merge(ifeature2, categoryFeatureRate, 
                        left_index = True, right_index = True, sort = False)
    
## COMBINE
    finalXy = pd.merge(xfeature, ifeature, how = 'left', 
                            left_index = True, right_index = True, sort = False)
    finalXy = pd.merge(finalXy, ufeature, how = 'left', 
                            left_index = True, right_index = True, sort = False)
    finalXy.fillna(0, inplace = True)
    finalItemFeature = ifeature2
##LABEL & RANDOM
    #merge X and y
    if (not target):
        labels = pd.read_csv(lfile, names = columns[0 : 2], 
                                index_col = ['user_id', 'item_id'])
        labels['buy'] = 1
        finalXy = pd.merge(finalXy, labels, how = 'left', 
                                left_index = True, right_index = True, sort = False)  
        finalXy.reset_index(inplace = True)
        
        labels = pd.read_csv(lfile, names = columns[0 : 2])
        labels.drop('user_id', axis = 1, inplace = True)
        labels.set_index('item_id', inplace = True)
        labels['buy'] = 1
        finalItemFeature = pd.merge(finalItemFeature, labels, how = 'left', 
                            left_index = True, right_index = True, sort = False) 
                            
        #random the zeros
        if (test == 0):
            ones = finalXy[finalXy['buy'] ==1]
            zeros = finalXy[finalXy['buy'].isnull()]
            zerosCount = (ratio - 1) * len(ones)
            zeros = zeros.ix[np.random.permutation(zeros.index)[ : zerosCount]]
            finalXy = pd.concat([ones, zeros])
            finalXy = finalXy.ix[np.random.permutation(finalXy.index)]
            
            ones = finalItemFeature[finalItemFeature['buy'] ==1]
            zeros = finalItemFeature[finalItemFeature['buy'].isnull()]
            zerosCount = (ratio - 1) * len(ones)
            zeros = zeros.ix[np.random.permutation(zeros.index)[ : zerosCount]]
            finalItemFeature = pd.concat([ones, zeros])
            finalItemFeature = finalItemFeature.ix[np.random.permutation(finalItemFeature.index)]
            
            
        finalXy.ix[ :, -1].to_csv(labelDay, na_rep = '0', 
                                    index = False, header = False)
        finalXy.ix[ :, : 2].to_csv(exampleDay, na_rep = '0', 
                                    index = False, header = False)
        finalXy.drop(['user_id', 'item_id', 'buy'], axis = 1, inplace = True)
        
        finalItemFeature.ix[ :, -1].to_csv(itemLabel, na_rep = '0', 
                                    index = True, header = True)
        finalItemFeature.drop('buy', inplace = True, axis = 1)
    else:
        # save target example
        finalXy.reset_index(inplace = True)

        finalXy.ix[ :, : 2].to_csv(examplefilename, na_rep = '0', 
                                    index = False, header = False)
        finalXy.drop(['user_id', 'item_id'], axis = 1, inplace = True)
#done, write into file
    finalXy.to_csv(featureDay, na_rep = '0', index = False, header = False)
    finalXy[ : 0].to_csv(featureName, na_rep = '0', index = False, header = True)
    finalItemFeature.to_csv(itemFeature, na_rep = '0', index = True, header = True)
##pandas end
    
    endTime = datetime.now()
    print (day, ' complete ', datetime.now())
    print (day , ' used time: ',  str(endTime - beginTime)) 
    print ('')

def test():
    extractFeature_Pandas('target', target = 1)
    input('>>')

if __name__ == '__main__': test()
