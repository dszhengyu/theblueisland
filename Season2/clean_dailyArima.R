run_online = T

runArima <- function(vec, order, predictDays = 30) {
  library("forecast")
  fit <- Arima(vec, order)
  pred <- forecast(fit, h = predictDays)
  predict <- pred$mean
  return (predict)
}


if (run_online == F) {
                                  header = F)
  purchaseTotal <- purchaseRedeemTotal$V2
  redeemTotal <- purchaseRedeemTotal$V3
} else {
  purchaseRedeemTotal <- dataset1
  purchaseTotal <- purchaseRedeemTotal$purchase
  redeemTotal <- purchaseRedeemTotal$redeem
}

purchasePredict <- runArima(purchaseTotal, c(3, 1, 3), 30)
redeemPredict <- runArima(redeemTotal, c(3, 1, 2), 30)

purchaseOnline <- purchasePredict
redeemOnline <- redeemPredict

startDate <- as.Date('2014-09-01')
report_date <- vector(length = 30)
for (i in 1 : 30) {
  report_date[i] <- as.numeric(strftime(startDate, format = '%Y%m%d'))
  startDate <- startDate + 1
}
online <- data.frame(report_date, purchaseOnline, redeemOnline)

if (run_online == F) {
              row.names = FALSE, col.names = FALSE, sep = ',')
}
dataname <- online
