from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from pandas import DataFrame

pwd = 'z:\\theblueisland\\'
day = '11_20'
target = 0
ratio = 3
prefix = pwd + "data_version2\\"
prefix2 = pwd + "feature_label2\\"
random = 1

ufile = prefix + "u_" + day + ".csv"
ifile = prefix + "i_" + day + ".csv"
lfile = prefix + "l_" + day + ".csv"
uptime = datetime.strptime('2014_' + day + ' 00:00:00', "%Y_%m_%d %H:%M:%S")
uptime += timedelta(days = 9, hours = 23)

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
xTotalFeature['4divall'] = xTotalFeature['x_total_4'] / xTotalFeature.sum(axis = 1)
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
# x_last2_3not4 = DataFrame(index = xTimeFeature[0].index)
# x_last2_3not4_index = np.logical_and(xTimeFeature[1][4] == 0, xTimeFeature[1][3] != 0)
# x_last2_3not4.ix[x_last2_3not4_index, 'x_last2_3not4'] = 1
# x_last2_3not4.fillna(0, inplace = True)

#every
xevery2= [(xTimeFeature[i] + xTimeFeature[i + 1]).add_prefix(str(i) + '_') 
            for i in range(0, 10, 2)]
xevery2 = pd.concat(xevery2, axis = 1).add_prefix('x_every2_')
#last
xlast1 = (xTimeFeature[0]).add_prefix('x_last_1')
xlast3 = (xTimeFeature[0] + xTimeFeature[1] + xTimeFeature[2]).add_prefix('x_last_3')
xlast5 = (xTimeFeature[0] + xTimeFeature[1] + xTimeFeature[2] 
            + xTimeFeature[3] + xTimeFeature[4]).add_prefix('x_last_5')
xT = pd.concat([xlast1, xlast3, xlast5], axis = 1)
xlast1_13 = xlast1.ix[ : , ['x_last_11', 'x_last_13']]
xlast3_13 = xlast3.ix[ : , ['x_last_31', 'x_last_33']]
xlast5_13 = xlast5.ix[ : , ['x_last_51', 'x_last_53']]
xT13 = pd.concat([xlast1_13, xlast3_13, xlast5_13], axis = 1)
#sum up
xTotalFeature = pd.concat([xTotalFeature13, xLastTimeFeature13, 
                xT13, xTotalFeature['4divall'], x_last1_3not4], axis = 1)
                    
## USER
# u active days
uSingleGroup = u.groupby(['user_id'])
uActiveDays = uSingleGroup['time'].nunique()
# total
uTotalGroup = u.groupby(['user_id', 'behavior_type'])
uTotalFeature = uTotalGroup['item_id'].count().unstack('behavior_type')
uTotalFeature.sort_index(axis = 1, inplace = True)
uTotalFeature = uTotalFeature.add_prefix('u_total_')
uTotalFeature.fillna(0, inplace = True)
#count() is total while nunique() is unique number
uTotalUnique = uTotalGroup['item_id'].nunique().unstack('behavior_type')
uTotalUnique.sort_index(axis = 1, inplace = True)
uTotalUnique = uTotalUnique.add_prefix('u_unique_')
uTotalUnique.fillna(0, inplace = True)
# item rate
uTotalFeature['average_1'] = uTotalFeature['u_total_1'] / uTotalUnique['u_unique_1']
uTotalFeature[uTotalFeature['average_1']  == np.inf] = 0
uTotalFeature['average_2'] = uTotalFeature['u_total_2'] / uTotalUnique['u_unique_2']
uTotalFeature[uTotalFeature['average_2']  == np.inf] = 0
uTotalFeature['average_3'] = uTotalFeature['u_total_3'] / uTotalUnique['u_unique_3']
uTotalFeature[uTotalFeature['average_3']  == np.inf] = 0
uTotalFeature['average_4'] = uTotalFeature['u_total_4'] / uTotalUnique['u_unique_4']
uTotalFeature[uTotalFeature['average_4']  == np.inf] = 0
# 4 div 1
uTotalFeature['4div1'] = uTotalFeature['u_total_4'].div(uTotalFeature['u_total_1'])
uTotalFeature[uTotalFeature['4div1'] == np.inf] = 0
# 4 div all
uTotalFeature['4divall'] = uTotalFeature['u_total_4'] / uTotalFeature.sum(axis = 1)
# 3 div 1
uTotalFeature['3div1'] = uTotalFeature['u_total_3'].div(uTotalFeature['u_total_1'])
uTotalFeature[uTotalFeature['3div1'] == np.inf] = 0
# 3 div all
uTotalFeature['3divall'] = uTotalFeature['u_total_3'] / uTotalFeature.sum(axis = 1)
# 4 div 3
uTotalFeature['4div3'] = uTotalFeature['u_total_4'].div(uTotalFeature['u_total_3'])
uTotalFeature[uTotalFeature['4div3'] == np.inf] = 0
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
#sum up
ufeature = pd.concat([uTotalFeature, uTotalUnique, uT, uActiveDays], axis = 1)
## ITEM
# total
i = pd.read_csv(ifile, names = columns, parse_dates = [5])
i['time'] = (uptime - i['time']).astype('timedelta64[D]')
iTotalGroup = i.groupby(['item_id', 'behavior_type'])
iTotalFeature = iTotalGroup['user_id'].count().unstack('behavior_type')
iTotalFeature.sort_index(axis = 1, inplace = True)
iTotalFeature = iTotalFeature.add_prefix('i_total_')
iTotalFeature.fillna(value = 0, inplace = True)
# i nunique()
iTotalUnique = iTotalGroup['user_id'].agg(lambda x: len(x.unique())).unstack('behavior_type')
iTotalUnique.sort_index(axis = 1, inplace = True)
iTotalUnique = iTotalUnique.add_prefix('i_unique_')
iTotalUnique.fillna(value = 0, inplace = True)
#rate
iTotalFeature['4divall'] = iTotalFeature['i_total_4'] / iTotalFeature.sum(axis = 1)
#last intersect
iLastTimeFeature = iTotalGroup['time'].min().unstack('behavior_type')
iLastTimeFeature.fillna(value = 10, inplace = True)
iLastTimeFeature.sort_index(axis = 1, inplace = True)
iLastTimeFeature = iLastTimeFeature.add_prefix('i_last_time_')
# time relative
iTimeGroup = u.groupby(['item_id', 'time', 'behavior_type'])
iTimeFeature = iTimeGroup['item_category'].count()
iTimeFeature = iTimeFeature.unstack(['time', 'behavior_type'])
iTimeFeature.sort_index(axis = 1, inplace = True)
iTimeFeature.fillna(value = 0, inplace = True)
#every
ievery2 = [(iTimeFeature[i] + iTimeFeature[i + 1]).add_prefix(str(i) + '_')
            for i in range(0, 10, 2)]
ievery2 = pd.concat(ievery2, axis = 1).add_prefix('i_every2_')
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
ifeature = pd.concat([iTotalFeature, iTotalUnique, iLastTimeFeature, ievery2, iT], axis = 1)
# no good, maybe a model for item among the whole time?
# ifeature['per_4'] = iTotalFeature['i_total_4'] / iTotalUnique['i_unique_4']
# ifeature['return_cunstom'] = iTotalFeature['i_total_4'] - iTotalUnique['i_unique_4']
# ifeature['return_cunstom'] /= iTotalUnique['i_unique_4']
# ifeature.fillna(0, inplace = True)

## COMBINE
finalXy = ufeature
# finalXy = pd.merge(xfeature, ifeature, how = 'left', 
#                         left_index = True, right_index = True, sort = False)
# finalXy = pd.merge(finalXy, ufeature, how = 'left', 
#                         left_index = True, right_index = True, sort = False)
finalXy.fillna(0, inplace = True)
##LABEL & RANDOM
# # merge X and y
# # x edition
# labels = pd.read_csv(lfile, names = columns[0 : 2], 
#                     index_col = ['user_id', 'item_id'])
# labels['buy'] = 1
# finalXy = pd.merge(finalXy, labels, how = 'left', 
#                     left_index = True, right_index = True, sort = False)  

# # item edition
# labels = pd.read_csv(lfile, names = columns[0 : 2])
# labels.drop('user_id', axis = 1, inplace = True)
# labels.set_index('item_id', inplace = True)
# labels['buy'] = 1
# finalXy = pd.merge(finalXy, labels, how = 'left', 
#                     left_index = True, right_index = True, sort = False) 

# user edition
labels = pd.read_csv(lfile, names = columns[0 : 2])
labels.drop('item_id', axis = 1, inplace = True)
labels.set_index('user_id', inplace = True)
labels['buy'] = 1
finalXy = pd.merge(finalXy, labels, how = 'left', 
                    left_index = True, right_index = True, sort = False) 

## ==
ones = finalXy[finalXy['buy'] ==1]
zeros = finalXy[finalXy['buy'].isnull()]

#done, write into file
finalXy[ : 0].to_csv(pwd + 'analyse_column_names.csv', na_rep = '0', index = True, header = True)