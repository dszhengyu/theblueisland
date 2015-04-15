from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from pandas import DataFrame

day = '12_8'
pwd = 'z:\\theblueisland\\'
prefix = pwd + "data_version2\\"
prefix2 = pwd + "rule\\"
ufile = prefix + "u_" + day + ".csv"
lfile = prefix + "l_" + day + ".csv"
ruleFile = prefix2 + 'rule.csv'
uptime = datetime.strptime('2014_' + day + ' 00:00:00', "%Y_%m_%d %H:%M:%S")
uptime += timedelta(days = 9, hours = 23)

columns = ['user_id', 'item_id', 'behavior_type', 
            'user_geohash', 'item_category', 'time']
            
u = pd.read_csv(ufile, names = columns, parse_dates = [5])
u['time'] = (uptime - u['time']).astype('timedelta64[D]')
u = u[u['time'] == 0]
uGroup = u.groupby(['user_id', 'item_id', 'behavior_type'])
uCount = uGroup['time'].count().unstack('behavior_type')
uCount.sort_index(axis = 1, inplace = True)
uCount = uCount[np.logical_and(uCount[3].notnull(), uCount[4].isnull())]
uCount.reset_index(inplace = True)
uCount.ix[ : , 'user_id' : 'item_id'].to_csv(ruleFile, index = False, header = False)

l = pd.read_csv(pwd + 'data_version2\\subItem.csv', 
                names = ['item_id', 'item_category'])
tmp = pd.merge(l, uCount)