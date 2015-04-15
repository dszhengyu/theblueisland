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
if (random == 1):
    featureDay = prefix2 + "feature_" + day + ".csv"
    labelDay = prefix2 + "label_" + day + ".csv"
else:
    featureDay = prefix2 + "test_feature_" + day + ".csv"
    labelDay = prefix2 + "test_label_" + day + ".csv"

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
#last intersect
xLastTimeFeature = xTotalGroup['time'].min().unstack('behavior_type')
xLastTimeFeature.sort_index(axis = 1, inplace = True)
xLastTimeFeature = xLastTimeFeature.add_prefix('x_last_time_')
#rate   ATTENTION: inf is replace by median
xTotalFeature['4div1'] = xTotalFeature['x_total_4'].div(xTotalFeature['x_total_1'])
xTotalFeature[xTotalFeature['4div1'] == np.inf] = xTotalFeature['4div1'].median()
#time relative
xTimeGroup = u.groupby(['user_id', 'item_id', 'time', 'behavior_type'])
xTimeFeature = xTimeGroup['item_category'].count()
xTimeFeature = xTimeFeature.unstack(['time', 'behavior_type'])
xTimeFeature.sort_index(axis = 1, inplace = True)
xTimeFeature.fillna(value = 0, inplace = True)
#every
xevery2= [xTimeFeature[i] + xTimeFeature[i + 1] for i in range(0, 10, 2)]
xevery2 = pd.concat(xevery2, axis = 1).add_prefix('x_every2_')
#last
xlast1 = (xTimeFeature[0]).add_prefix('x_last_1')
xlast3 = (xTimeFeature[0] + xTimeFeature[1] + xTimeFeature[2]).add_prefix('x_last_3')
xlast5 = (xlast3 + xTimeFeature[3] + xTimeFeature[4]).add_prefix('x_last_5')
xT = pd.concat([xlast1, xlast3, xlast5], axis = 1)
#sum up
xTotalFeature = pd.concat([xTotalFeature, xLastTimeFeature, xevery2, xT], axis = 1)

## USER
# total
uTotalGroup = u.groupby(['user_id', 'behavior_type'])
uTotalFeature = uTotalGroup['item_id'].count().unstack('behavior_type')
uTotalFeature.sort_index(axis = 1, inplace = True)
#count() is total while nunique() is unique number
uTotalFeature = uTotalFeature.add_prefix('u_total_')
uTotalFeature.fillna(0, inplace = True)
#last intersect
uLastTimeFeature = uTotalGroup['time'].min().unstack('behavior_type')
uLastTimeFeature.sort_index(axis = 1, inplace = True)
uLastTimeFeature = uLastTimeFeature.add_prefix('u_last_time_')
#rate   ATTENTION: inf is replace by median
uTotalFeature['4div1'] = uTotalFeature['u_total_4'].div(uTotalFeature['u_total_1'])
uTotalFeature[uTotalFeature['4div1'] == np.inf] = uTotalFeature['4div1'].median()
# #time relative
# uTimeGroup = u.groupby(['user_id', 'time', 'behavior_type'])
# uTimeFeature = uTimeGroup['item_category'].count()
# uTimeFeature = uTimeFeature.unstack(['time', 'behavior_type'])
# uTimeFeature.sort_index(axis = 1, inplace = True)
# uTimeFeature.fillna(value = 0, inplace = True)
# #last
# ulast1 = uTimeFeature[0]
# ulast3 = uTimeFeature[0] + uTimeFeature[1] + uTimeFeature[2]
# ulast5 = ulast3 + uTimeFeature[3] + uTimeFeature[4]
# uT = pd.concat([ulast1, ulast3, ulast5], axis = 1)
#sum up
uTotalFeature = pd.concat([uTotalFeature, uLastTimeFeature], axis = 1)
## ITEM
# total
i = pd.read_csv(ifile, names = columns, parse_dates = [5])
i['time'] = (uptime - i['time']).astype('timedelta64[D]')
iTotalGroup = i.groupby(['item_id', 'behavior_type'])
iTotalFeature = iTotalGroup['user_id'].count().unstack('behavior_type')
iTotalFeature.sort_index(axis = 1, inplace = True)
iTotalFeature = iTotalFeature.add_prefix('item_total_')
#last intersect
iLastTimeFeature = iTotalGroup['time'].min().unstack('behavior_type')
iLastTimeFeature.sort_index(axis = 1, inplace = True)
iLastTimeFeature = iLastTimeFeature.add_prefix('i_last_time_')
# time relative
iTimeGroup = u.groupby(['item_id', 'time', 'behavior_type'])
iTimeFeature = iTimeGroup['item_category'].count()
iTimeFeature = iTimeFeature.unstack(['time', 'behavior_type'])
iTimeFeature.sort_index(axis = 1, inplace = True)
iTimeFeature.fillna(value = 0, inplace = True)
# #every
# ievery2 = [iTimeFeature[i] + iTimeFeature[i + 1] for i in range(0, 10, 2)]
# ievery2 = pd.concat(ievery2, axis = 1).add_prefix('i_every2_')
#last
ilast1 = iTimeFeature[0]
ilast3 = iTimeFeature[0] + iTimeFeature[1] + iTimeFeature[2]
ilast5 = ilast3 + iTimeFeature[3] + iTimeFeature[4]
iT = pd.concat([ilast1, ilast3, ilast5], axis = 1)
#sum up
iTotalFeature = pd.concat([iTotalFeature, iLastTimeFeature, iT], axis = 1)

## COMBINE
finalXy = pd.merge(xTotalFeature, iTotalFeature, how = 'left', 
                        left_index = True, right_index = True, sort = False)
finalXy = pd.merge(finalXy, uTotalFeature, how = 'left', 
                        left_index = True, right_index = True, sort = False)
finalXy.fillna(0, inplace = True)
##LABEL & RANDOM
#merge X and y
labels = pd.read_csv(lfile, names = columns[0 : 2], 
                    index_col = ['user_id', 'item_id'])
labels['buy'] = 1
finalXy = pd.merge(finalXy, labels, how = 'left', 
                    left_index = True, right_index = True, sort = False)  
ones = finalXy[finalXy['buy'] ==1]
zeros = finalXy[finalXy['buy'].isnull()]

#done, write into file
finalXy.to_csv(featureDay, na_rep = '0', index = False, header = False)