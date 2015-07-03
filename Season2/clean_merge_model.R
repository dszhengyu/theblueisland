run_online = T

if (run_online == F) {
  
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
}

dataname <- mergeOnline