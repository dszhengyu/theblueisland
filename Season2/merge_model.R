run_online = F

if (run_online == F) {
  dailyARIMA <- read.csv('z:\\theblueisland\\Season2\\online_dailyARIMA.csv')
  dot_for_all <- read.csv('z:\\theblueisland\\Season2\\online_dot_for_all.csv')
  #dailyANN <- read.csv('z:\\theblueisland\\Season2\\online_dailyANN.csv')
  
  purchaseMerge <- 0.5 * dailyARIMA$purchaseOnline + 0.5 * dot_for_all$purchaseOnline
  redeemMerge <- 0.5 * dailyARIMA$redeemOnline + 0.5 * dot_for_all$redeemOnline
} else {
  dailyARIMA <- dataset1
  dot_for_all <- dataset2
  
  purchaseMerge <- 0.5 * dailyARIMA$purchaseonline + 0.5 * dot_for_all$purchaseonline
  redeemMerge <- 0.5 * dailyARIMA$redeemonline + 0.5 * dot_for_all$redeemonline
}

report_date <- dailyARIMA$report_date

mergeOnline <- data.frame(report_date, purchaseMerge, redeemMerge)

if (run_online == F) {
  write.table(x = mergeOnline, file = 'z:\\theblueisland\\Season2\\online_merge.csv', row.names = FALSE, sep = ',')
}

dataname <- mergeOnline