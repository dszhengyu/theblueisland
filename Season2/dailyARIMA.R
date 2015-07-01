run_online = F

runArima <- function(vec, order, seasonal, predictDays = 30) {
  library("forecast")
  fit <- Arima(vec, order = order, seasonal = list(order = seasonal, period = 7))
  pred <- forecast(fit, h = predictDays)
  #plot(pred)
  predict <- pred$mean
  return (predict)
}

############ subroutine up there ########

if (run_online == F) {
  purchaseRedeemTotal <- read.csv('z:\\theblueisland\\Season2\\daily_purchase_redeem.csv')
} else {
  purchaseRedeemTotal <- dataset1
}

# choose date from 2013-11-01
purchaseRedeemTotal <- purchaseRedeemTotal[124 : 427, ]

purchaseTotal <- purchaseRedeemTotal$purchase
redeemTotal <- purchaseRedeemTotal$redeem

purchasePredict <- runArima(purchaseTotal, c(6, 1, 5), c(1, 1, 0), 30)
redeemPredict <- runArima(redeemTotal, c(2, 1, 2), c(1, 1, 0), 30)

purchaseOnline <- purchasePredict
redeemOnline <- redeemPredict
####### merge online set $$$$$$$$$$$$$$

startDate <- as.Date('2014-09-01')
report_date <- vector(length = 30)
for (i in 1 : 30) {
  report_date[i] <- as.numeric(strftime(startDate, format = '%Y%m%d'))
  startDate <- startDate + 1
}
online <- data.frame(report_date, purchaseOnline, redeemOnline)

if (run_online == F) {
  write.table(x = online, file = 'z:\\theblueisland\\Season2\\tc_comp_predict_table.csv', row.names = FALSE, col.names = FALSE, sep = ',')
}
dataname <- online
