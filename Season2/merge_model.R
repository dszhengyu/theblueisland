run_online = F

if (run_online == F) {
  dailyARIMA <- read.csv('z:\\theblueisland\\Season2\\online_dailyARIMA.csv')
  dot_for_all <- read.csv('z:\\theblueisland\\Season2\\online_dot_for_all.csv')
  baseline <- read.csv('z:\\theblueisland\\Season2\\online_baseline.csv')
  
  purchaseMerge <- 0.2 * dailyARIMA$purchaseOnline + 0.2 * dot_for_all$purchaseOnline + 0.6 * baseline$purchaseOnline
  redeemMerge <- 0.2 * dailyARIMA$redeemOnline + 0.2 * dot_for_all$redeemOnline + 0.6 * baseline$redeemOnline
  
} else {
  dailyARIMA <- dataset1
  dot_for_all <- dataset2
  baseline <- dataset3
  
  purchaseMerge <- 0.2 * dailyARIMA$purchaseonline + 0.2 * dot_for_all$purchaseonline + 0.6 * baseline$purchaseonline
  redeemMerge <- 0.2 * dailyARIMA$redeemonline + 0.2 * dot_for_all$redeemonline + 0.6 * baseline$redeemonline
}

report_date <- dailyARIMA$report_date

mergeOnline <- data.frame(report_date, purchaseMerge, redeemMerge)

if (run_online == F) {
  write.table(x = mergeOnline, file = 'z:\\theblueisland\\Season2\\online_merge.csv', row.names = FALSE, sep = ',')
}

dataname <- mergeOnline