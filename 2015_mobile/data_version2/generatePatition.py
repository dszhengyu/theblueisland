date1List = ['11' + '-' + str(day) for day in range(18, 31)]
date1List += ['12' + '-' + str(day) for day in range(1, 8)]

date2List = ['11' + '_' + str(day) for day in range(18, 31)]
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


f = open('z:\\theblueisland\\data_version2\\tmp.sql', 'w')
for j in date2List:
    s = open('z:\\theblueisland\\data_version2\\partition_' + j + '.sql').readlines()
    s = ''.join(s)
    f.write(s)
f.close()


str = open('z:\\theblueisland\\analyse.txt').readlines()
file = open('z:\\theblueisland\\sentence.txt', 'w')
s = [i for i in str if i[ : 2] == 'In']
ss = [i.split(']: ')[1 : ] for i in s]
sss = [i[0] for i in ss]
ssss = ''.join(sss)
file.write(ssss)
file.close()