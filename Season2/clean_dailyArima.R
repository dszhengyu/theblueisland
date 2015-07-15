run_online = T

runArima <- function(vec, order, seasonal, predictDays = 30) {
  library("forecast")
  fit <- Arima(vec, order = order, seasonal = list(order = seasonal, period = 7))
  pred <- forecast(fit, h = predictDays)
  predict <- pred$mean
  return (predict)
}


if (run_online == F) {
} else {
  purchaseRedeemTotal <- dataset1
}

localPurchaseRedeemTotal <- purchaseRedeemTotal[244 : 396, ]

localPurchaseTotal <- localPurchaseRedeemTotal$purchase
localRedeemTotal <- localPurchaseRedeemTotal$redeem

purchasePredict <- runArima(localPurchaseTotal, c(0, 1, 2), c(1, 1, 0), 31)
redeemPredict <- runArima(localRedeemTotal, c(2, 1, 2), c(1, 1, 0), 31)

purchaseLocal <- purchasePredict
redeemLocal <- redeemPredict

onlinePurchaseRedeemTotal <- purchaseRedeemTotal[244 : 427, ]

onlinePurchaseTotal <- onlinePurchaseRedeemTotal$purchase
onlineRedeemTotal <- onlinePurchaseRedeemTotal$redeem

purchasePredict <- runArima(onlinePurchaseTotal, c(0, 1, 2), c(1, 1, 0), 30)
redeemPredict <- runArima(onlineRedeemTotal, c(2, 1, 2), c(1, 1, 0), 30)

purchaseOnline <- purchasePredict
redeemOnline <- redeemPredict


startDate <- as.Date('2014-08-01')
report_date <- vector(length = 31)
for (i in 1 : 31) {
  report_date[i] <- as.numeric(strftime(startDate, format = '%Y%m%d'))
  startDate <- startDate + 1
}
local <- data.frame(report_date, purchaseLocal, redeemLocal)

if (run_online == F) {
}

startDate <- as.Date('2014-09-01')
report_date <- vector(length = 30)
for (i in 1 : 30) {
  report_date[i] <- as.numeric(strftime(startDate, format = '%Y%m%d'))
  startDate <- startDate + 1
}
online <- data.frame(report_date, purchaseOnline, redeemOnline)

if (run_online == F) {
}
dataname <- online
