import pandas as pd

purchaseRedeemTotal = pd.read_csv('z:\\theblueisland\\Season2\\daily_purchase_redeem.csv',
                            names = ['report_date', 'total_purchase_amt', 'total_redeem_amt'], 
                            parse_dates = ['report_date'], index_col = ['report_date'])
purchaseRedeemTotal.plot()

## clean R script

files = ['dailyArima.R', 'dailyANN.R', 'dot_for_all.R', 'merge_model.R']

for file in files:
    badChar = ['#', 'cat', 'print', 'plot', 'lines']
    rFile = open('z:\\theblueisland\\Season2\\' + file).readlines()
    rFileNoComment = [line for line in rFile if 
                        '#' not in line and
                        'cat' not in line and
                        'print' not in line and
                        'plot' not in line and
                        'lines' not in line and
                        'theblueisland' not in line]
    rFileNoComment.pop(0)
    rFileNoComment.insert(0, 'run_online = T\n')
    rFileClean = open('z:\\theblueisland\\Season2\\clean_' + file, 'w')
    rFileClean.write(''.join(rFileNoComment))
    rFileClean.close()

## compare online set

allMethod = ['dailyANN', 'dailyARIMA', 'dot_for_all', 'merge']

for localSingle in allMethod:
        predictLocal = pd.read_csv('z:\\theblueisland\\Season2\\local_' + localSingle + '.csv',
                                parse_dates = ['report_date'], index_col = ['report_date'])
    predictLocal.plot(title = localSingle)

for onlineSingle in allMethod:
    predictOnline = pd.read_csv('z:\\theblueisland\\Season2\\online_' + onlineSingle + '.csv',
                                parse_dates = ['report_date'], index_col = ['report_date'])
    predictOnline.plot(title = onlineSingle)
