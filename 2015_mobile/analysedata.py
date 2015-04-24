from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.feature_selection import SelectKBest, SelectPercentile, chi2
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import f1_score, classification_report, precision_score
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import StratifiedKFold

pwd = 'z:\\theblueisland\\'
day = '11_20'
prefix = pwd + "data_version2\\"

ufile = prefix + "u_" + day + ".csv"
ifile = prefix + "i_" + day + ".csv"
lfile = prefix + "l_" + day + ".csv"
uptime = datetime.strptime('2014_' + day + ' 00:00:00', "%Y_%m_%d %H:%M:%S")
uptime += timedelta(days = 9, hours = 23)
columns = ['user_id', 'item_id', 'behavior_type', 
            'user_geohash', 'item_category', 'time']
## X
#X, total
def xConstructFeature():
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
    # 4 div 3
    xTotalFeature['x_4div3'] = xTotalFeature['x_total_4'].div(xTotalFeature['x_total_3'])
    xTotalFeature[xTotalFeature['x_4div3'] == np.inf] = 0
    xTotalFeature.fillna(0, inplace = True)
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
    xT = pd.concat([xlast1, xlast2, xlast3, xlast4, xlast5], axis = 1)
    xlast1_13 = xlast1.ix[ : , ['x_last_11', 'x_last_13']]
    xlast2_13 = xlast2.ix[ : , ['x_last_21', 'x_last_23']]
    xlast3_13 = xlast3.ix[ : , ['x_last_31', 'x_last_33']]
    xlast4_13 = xlast4.ix[ : , ['x_last_41', 'x_last_43']]
    xlast5_13 = xlast5.ix[ : , ['x_last_51', 'x_last_53']]
    xT13 = pd.concat([xlast1_13, xlast2_13, xlast3_13, xlast4_13, xlast5_13], axis = 1)
    #sum up
    xfeature = pd.concat([xTotalFeature13, xLastTimeFeature13, xT13,
                        xTotalFeature['x_3div1'], xTotalFeature['x_4divall'],
                        xTotalFeature['x_4div1'], xTotalFeature['x_3divall'], 
                        x_last1_3not4, x_last2_3not4, x_last3_3not4], axis = 1)
    return xfeature
## USER
# total
def uConstructFeature():
    u = pd.read_csv(ufile, names = columns, parse_dates = [5])
    u['time'] = uptime - u['time']
    u['timeD'] = u['time'].astype('timedelta64[D]')
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
    # # item rate
    # uTotalFeature['u_average_1'] = uTotalFeature['u_total_1'] / uTotalUnique['u_unique_1']
    # uTotalFeature[uTotalFeature['u_average_1']  == np.inf] = 0
    # uTotalFeature['u_average_3'] = uTotalFeature['u_total_3'] / uTotalUnique['u_unique_3']
    # uTotalFeature[uTotalFeature['u_average_3']  == np.inf] = 0
    # # 4 div 1
    # uTotalFeature['u_4div1'] = uTotalFeature['u_total_4'].div(uTotalFeature['u_total_1'])
    # uTotalFeature[uTotalFeature['u_4div1'] == np.inf] = 0
    # # 4 div all
    # uTotalFeature['u_4divall'] = uTotalFeature['u_total_4'] / uTotalFeature.sum(axis = 1)
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
    #last
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
    uT134 = pd.concat([ulast1_3, ulast2_3, ulast3_13, ulast5_134], 
                        axis = 1)
    #sum up
    ufeature = pd.concat([uTotalFeature134, uTotalFeature['u_3div1'], 
                            uTotalFeature['u_3divall'], uTotalFeature['u_4div3'],
                            uTotalUnique14, uT134], axis = 1)
    return ufeature
## ITEM
# total
def iConstructFeature():
    i = pd.read_csv(ifile, names = columns, parse_dates = [5])
    i['time'] = uptime - i['time']
    i['timeD'] = i['time'].astype('timedelta64[D]')
    iTotalGroup = i.groupby(['item_id', 'behavior_type'])
    iTotalFeature = iTotalGroup['user_id'].count().unstack('behavior_type')
    iTotalFeature.sort_index(axis = 1, inplace = True)
    iTotalFeature = iTotalFeature.add_prefix('i_total_')
    iTotalFeature.fillna(value = 0, inplace = True)
    iTotalFeature3 = iTotalFeature['i_total_3']
    # i nunique()
    iTotalUnique = iTotalGroup['user_id'].agg(lambda x: len(x.unique())).unstack('behavior_type')
    iTotalUnique.sort_index(axis = 1, inplace = True)
    iTotalUnique = iTotalUnique.add_prefix('i_unique_')
    iTotalUnique.fillna(value = 0, inplace = True)
    iTotalUnique3 = iTotalUnique['i_unique_3']
    # 4 div 1
    iTotalFeature['i_4div1'] = iTotalFeature['i_total_4'].div(iTotalFeature['i_total_1'])
    iTotalFeature[iTotalFeature['i_4div1'] == np.inf] = 0
    # 3 div 1
    iTotalFeature['i_3div1'] = iTotalFeature['i_total_3'].div(iTotalFeature['i_total_1'])
    iTotalFeature[iTotalFeature['i_3div1'] == np.inf] = 0
    # 3 div all
    iTotalFeature['i_3divall'] = iTotalFeature['i_total_3'] / iTotalFeature.sum(axis = 1)
    # 4 div 3
    iTotalFeature['i_4div3'] = iTotalFeature['i_total_4'].div(iTotalFeature['i_total_3'])
    iTotalFeature[iTotalFeature['i_4div3'] == np.inf] = 0
    iTotalFeature.fillna(0, inplace = True)
    #last intersect
    iLastTimeFeature = iTotalGroup['timeD'].min().unstack('behavior_type')
    iLastTimeFeature.fillna(value = 10, inplace = True)
    iLastTimeFeature.sort_index(axis = 1, inplace = True)
    iLastTimeFeature = iLastTimeFeature.add_prefix('i_last_time_')
    iLastTimeFeature13 = iLastTimeFeature.ix[ : , ['i_last_time_1', 'i_last_time_3']]
    # timeD relative
    iTimeGroup = i.groupby(['item_id', 'timeD', 'behavior_type'])
    iTimeFeature = iTimeGroup['item_category'].count()
    iTimeFeature = iTimeFeature.unstack(['timeD', 'behavior_type'])
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
    ilast1_13 = ilast1.ix[:, ['i_last_11', 'i_last_13']]
    ilast3_13 = ilast3.ix[:, ['i_last_31', 'i_last_33']]
    ilast5_13 = ilast5.ix[:, ['i_last_51', 'i_last_53']]
    iT13 = pd.concat([ilast1_13, ilast3_13, ilast5_13], axis = 1)
    #sum up
    ifeature = pd.concat([iTotalFeature3, iTotalUnique3, 
                        iTotalFeature['i_3divall'], iLastTimeFeature13, 
                        iT13], axis = 1)
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
    
    return ifeature

## start analyse bellow
def xAnalyse():
    xfeature = xConstructFeature()
    finalXy = xfeature
    # x edition
    labels = pd.read_csv(lfile, names = columns[0 : 2], 
                        index_col = ['user_id', 'item_id'])
    labels['buy'] = 1
    finalXy = pd.merge(finalXy, labels, how = 'left', 
                        left_index = True, right_index = True, sort = False)
    ones = finalXy[finalXy['buy'] ==1]
    zeros = finalXy[finalXy['buy'].isnull()]
    #done, write into file
    finalXy[ : 0].to_csv(pwd + 'analyse_column_names.csv', na_rep = '0', index = True, header = True)
    
    x_total = ones.ix[ : , 'x_total_1' : 'x_total_4']
    print (x_total.describe())
    zero_x_total = zeros.ix[ : , 'x_total_1' : 'x_total_4']
    print (zero_x_total.describe())
    print ()
    
    x_last_time = ones.ix[ : , 'x_last_time_1' : 'x_last_time_4']
    zero_x_last_time = zeros.ix[ : , 'x_last_time_1' : 'x_last_time_4']
    print (x_last_time.describe())
    print (zero_x_last_time.describe())
    print ()
    
    x_last = ones.ix[ : , 'x_last_11' : 'x_last_54']
    zero_x_last = zeros.ix[ : , 'x_last_11' : 'x_last_54']
    print (x_last.describe())
    print (zero_x_last.describe())
    print ()
    
    x_rate = ones.ix[ : , ['x_4divall', 'x_4div1', 'x_3div1', 'x_3divall', 'x_4div3']]
    zero_rate = zeros.ix[ : , ['x_4divall', 'x_4div1', 'x_3div1', 'x_3divall', 'x_4div3']]
    print (x_rate.describe())
    print (zero_rate.describe())
    print ()
    
    x_last3_3not4 = ones['x_last3_3not4']
    zero_x_last3_3not4 = zeros['x_last3_3not4']
    print (x_last3_3not4.describe())
    print (zero_x_last3_3not4.describe())
    print ()
    x_last2_3not4 = ones['x_last2_3not4']
    zero_x_last2_3not4 = zeros['x_last2_3not4']
    print (x_last2_3not4.describe())
    print (zero_x_last2_3not4.describe())
    print ()
    x_last1_3not4 = ones['x_last1_3not4']
    zero_x_last1_3not4 = zeros['x_last1_3not4']
    print (x_last1_3not4.describe())
    print (zero_x_last1_3not4.describe())
    print ()
    
    
def iAnalyse():
    ifeature = iConstructFeature()
    finalXy = ifeature
    # item edition
    labels = pd.read_csv(lfile, names = columns[0 : 2])
    labels.drop('user_id', axis = 1, inplace = True)
    labels.set_index('item_id', inplace = True)
    labels['buy'] = 1
    finalXy = pd.merge(finalXy, labels, how = 'left', 
                        left_index = True, right_index = True, sort = False) 
    ones = finalXy[finalXy['buy'] ==1]
    zeros = finalXy[finalXy['buy'].isnull()]
    #done, write into file
    finalXy[ : 0].to_csv(pwd + 'analyse_column_names.csv', na_rep = '0', index = True, header = True)
    
    i_total = ones.ix[ : , 'i_total_1' : 'i_total_4']
    zero_i_total = zeros.ix[ : , 'i_total_1' : 'i_total_4']
    print (i_total.describe())
    print (zero_i_total.describe())
    print ()
    
    i_last = ones.ix[ : , 'i_last_time_1' : 'i_last_time_4']
    zero_i_last = zeros.ix[ : , 'i_last_time_1' : 'i_last_time_4']
    print (i_last.describe())
    print (zero_i_last.describe())
    print ()
    
    i_last = ones.ix[ : , 'i_last_11' : 'i_last_54']
    zero_i_last = zeros.ix[ : , 'i_last_11' : 'i_last_54']
    print (i_last.describe())
    print (zero_i_last.describe())
    print ()
    
    i_unique = ones.ix[ : , 'i_unique_1' : 'i_unique_4']
    zero_i_unique = zeros.ix[ : , 'i_unique_1' : 'i_unique_4']
    print (i_unique.describe())
    print (zero_i_unique.describe())
    print ()

    i_rate = ones.ix[ : , ['i_4divall', 'i_4div1', 'i_3div1', 'i_3divall', 'i_4div3']]
    zero_i_rate = zeros.ix[ : , ['i_4divall', 'i_4div1', 'i_3div1', 'i_3divall', 'i_4div3']]
    print (i_rate.describe())
    print (zero_i_rate.describe())
    print ()
    
    c_total = ones.ix[ : , 'c_total_1' : 'c_total_4']
    zero_c_total = zeros.ix[ : , 'c_total_1' : 'c_total_4']
    print (c_total.describe())
    print (zero_c_total.describe())
    print ()
    
    c_i_total = ones.ix[ : , 'c_i_total_1' : 'c_i_total_4']
    zero_c_i_total = zeros.ix[ : , 'c_i_total_1' : 'c_i_total_4']
    print (c_i_total.describe())
    print (zero_c_i_total.describe())
    print ()
    
    c_i_rate = ones.ix[ : , 'c_i_rate_1' : 'c_i_rate_4']
    zero_c_i_rate = zeros.ix[ : , 'c_i_rate_1' : 'c_i_rate_4']
    print (c_i_rate.describe())
    print (zero_c_i_rate.describe())
    print ()

def uAnalyse():
    ufeature = uConstructFeature()
    finalXy = ufeature
    # user edition
    labels = pd.read_csv(lfile, names = columns[0 : 2])
    labels.drop('item_id', axis = 1, inplace = True)
    labels.set_index('user_id', inplace = True)
    labels['buy'] = 1
    finalXy = pd.merge(finalXy, labels, how = 'left', 
                        left_index = True, right_index = True, sort = False) 
    ones = finalXy[finalXy['buy'] ==1]
    zeros = finalXy[finalXy['buy'].isnull()]
    #done, write into file
    finalXy[ : 0].to_csv(pwd + 'analyse_column_names.csv', 
                        na_rep = '0', index = True, header = True)
    
    u_total = ones.ix[ : , 'u_total_1' : 'u_total_4']
    zero_u_total = zeros.ix[ : , 'u_total_1' : 'u_total_4']
    print (u_total.describe())
    print (zero_u_total.describe())
    print ()
    
    u_unique = ones.ix[ : , 'u_unique_1' : 'u_unique_4']
    zero_u_unique = zeros.ix[ : , 'u_unique_1' : 'u_unique_4']
    print (u_unique.describe())
    print (zero_u_unique.describe())
    print ()
    
    u_rate = ones.ix[ : , ['u_4div1', 'u_4divall', 'u_3div1', 'u_3divall', 'u_4div3']]
    zero_u_rate = zeros.ix[ : , ['u_4div1', 'u_4divall', 'u_3div1', 'u_3divall', 'u_4div3']]
    print (u_rate.describe())
    print (zero_u_rate.describe())
    print ()
    
    u_last = ones.ix[ : , 'u_last_11' : 'u_last_54']
    zero_u_last = zeros.ix[ : , 'u_last_11' : 'u_last_54']
    print (u_last.describe())
    print (zero_u_last.describe())
    print ()
    
def test():
    uAnalyse()
    
def featureSelect ():
    ufeature = uConstructFeature()
    ifeature = iConstructFeature()
    xfeature = xConstructFeature()
    finalXy = pd.merge(xfeature, ifeature, how = 'left', 
                            left_index = True, right_index = True, sort = False)
    finalXy = pd.merge(finalXy, ufeature, how = 'left', 
                            left_index = True, right_index = True, sort = False)
    finalXy.fillna(0, inplace = True)
    labels = pd.read_csv(lfile, names = columns[0 : 2], 
                        index_col = ['user_id', 'item_id'])
    labels['buy'] = 1
    finalXy = pd.merge(finalXy, labels, how = 'left', 
                        left_index = True, right_index = True, sort = False) 
    finalXy.fillna(0, inplace = True)
    X = finalXy.ix[ : , : -1]
    y = finalXy['buy']
    slt = SelectKBest(chi2, k = 10)
    slt.fit(X, y)
    # clf = RandomForestClassifier()
    # param = {'n_estimators' : [10, 25, 40, 50, 60, 70],
    #             'max_depth' : [6, 7, 8, 9, 10, None]}
    # clf = GridSearchCV(estimator = clf, param_grid = param, 
    #                     scoring = 'f1', 
    #                     cv = StratifiedKFold(y, 3), 
    #                     verbose = 3, pre_dispatch = '3*n_jobs')
    # clf.fit(X, y)
    # clf = clf.best_estimator_
    # y_pred = clf.predict(X)
    # print (classification_report(y, y_pred))
    scoreList = DataFrame(columns = X.columns)
    scoreList.loc['SelectKBest_score'] = slt.scores_
    scoreList.loc['SelectKBest_pvalues'] = slt.pvalues_
    # scoreList.loc['RF_feature_importances'] = clf.feature_importances_
    scoreList = scoreList.stack().unstack(0)
    scoreList.to_csv(pwd + 'selection2.csv')
    
    
if __name__ == '__main__': featureSelect()
    
##old code bellow
    
# ## COMBINE
# finalXy = ifeature
# # finalXy = pd.merge(xfeature, ifeature, how = 'left', 
# #                         left_index = True, right_index = True, sort = False)
# # finalXy = pd.merge(finalXy, ufeature, how = 'left', 
# #                         left_index = True, right_index = True, sort = False)
# finalXy.fillna(0, inplace = True)
# ##LABEL & RANDOM
# # merge X and y
# # # x edition
# # labels = pd.read_csv(lfile, names = columns[0 : 2], 
# #                     index_col = ['user_id', 'item_id'])
# # labels['buy'] = 1
# # finalXy = pd.merge(finalXy, labels, how = 'left', 
# #                     left_index = True, right_index = True, sort = False)  
# 
# # item edition
# labels = pd.read_csv(lfile, names = columns[0 : 2])
# labels.drop('user_id', axis = 1, inplace = True)
# labels.set_index('item_id', inplace = True)
# labels['buy'] = 1
# finalXy = pd.merge(finalXy, labels, how = 'left', 
#                     left_index = True, right_index = True, sort = False) 
# 
# # # user edition
# # labels = pd.read_csv(lfile, names = columns[0 : 2])
# # labels.drop('item_id', axis = 1, inplace = True)
# # labels.set_index('user_id', inplace = True)
# # labels['buy'] = 1
# # finalXy = pd.merge(finalXy, labels, how = 'left', 
# #                     left_index = True, right_index = True, sort = False) 
# 
# ## ==
# ones = finalXy[finalXy['buy'] ==1]
# zeros = finalXy[finalXy['buy'].isnull()]
# 
# #done, write into file
# finalXy[ : 0].to_csv(pwd + 'analyse_column_names.csv', na_rep = '0', index = True, header = True)
# 
# ## get final analyse
# 
# ## X analyse
