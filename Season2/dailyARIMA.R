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

# local
localPurchaseRedeemTotal <- purchaseRedeemTotal[124 : 396, ]

localPurchaseTotal <- localPurchaseRedeemTotal$purchase
localRedeemTotal <- localPurchaseRedeemTotal$redeem

purchasePredict <- runArima(localPurchaseTotal, c(6, 1, 5), c(1, 1, 0), 31)
redeemPredict <- runArima(localRedeemTotal, c(2, 1, 2), c(1, 1, 0), 31)

purchaseLocal <- purchasePredict
redeemLocal <- redeemPredict

# online
# choose date from 2013-11-01
onlinePurchaseRedeemTotal <- purchaseRedeemTotal[124 : 427, ]

onlinePurchaseTotal <- onlinePurchaseRedeemTotal$purchase
onlineRedeemTotal <- onlinePurchaseRedeemTotal$redeem

purchasePredict <- runArima(onlinePurchaseTotal, c(6, 1, 5), c(1, 1, 0), 30)
redeemPredict <- runArima(onlineRedeemTotal, c(2, 1, 2), c(1, 1, 0), 30)

purchaseOnline <- purchasePredict
redeemOnline <- redeemPredict


########$$$$$$$$$$$$$$$$$$$$$ merge local online set $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$########
startDate <- as.Date('2014-08-01')
report_date <- vector(length = 31)
for (i in 1 : 31) {
  report_date[i] <- as.numeric(strftime(startDate, format = '%Y%m%d'))
  startDate <- startDate + 1
}
local <- data.frame(report_date, purchaseLocal, redeemLocal)

if (run_online == F) {
  write.table(x = local, file = 'z:\\theblueisland\\Season2\\local_dailyARIMA.csv', row.names = FALSE, sep = ',')
}

startDate <- as.Date('2014-09-01')
report_date <- vector(length = 30)
for (i in 1 : 30) {
  report_date[i] <- as.numeric(strftime(startDate, format = '%Y%m%d'))
  startDate <- startDate + 1
}
online <- data.frame(report_date, purchaseOnline, redeemOnline)

if (run_online == F) {
  write.table(x = online, file = 'z:\\theblueisland\\Season2\\online_dailyARIMA.csv', row.names = FALSE, sep = ',')
}
dataname <- online
