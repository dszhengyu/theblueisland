date1List = ['11' + '-' + str(day) for day in range(24, 31)]
date1List += ['12' + '-' + str(day) for day in range(1, 8)]

date2List = ['11' + '_' + str(day) for day in range(24, 31)]
date2List += ['12' + '_' + str(day) for day in range(1, 8)]


s = open('partition_11_18.sql').readlines()
s = ''.join(s)
s = s.replace('%', '%%')
s = s.replace('11-18', '%(date1)s')
s = s.replace('11_18', '%(date2)s')

for i, j in zip(date1List, date2List):
    f = open('partition_' + j + '.sql', 'w')
    f.write(s % {'date1': i, 'date2': j})
    f.close()
