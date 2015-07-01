# orderUsed = c(2, 1, 2)
# seasonalUsed = c(1, 1, 0)
# predictDays = 31
# auto = 0

train <- read.csv('z:\\theblueisland\\R\\trainFileARIMA.csv', header = FALSE)
if (auto == 0) {
  library('stats')
  fit <-arima(train, order = orderUsed, seasonal = list(order = seasonalUsed, period = 7))
  pre <- predict(fit, predictDays)
  predict <- pre[["pred"]]
  
} else {
  library('forecast')
  fit <-auto.arima(train, start.p = 5, start.q = 5)
  pre <- forecast(fit, h = predictDays)
  predict <- pre$mean
}

write.csv(predict, 'z:\\theblueisland\\R\\predictFileARIMA.csv', row.names = FALSE)
write.csv(residuals(fit), 'z:\\theblueisland\\R\\residualsFileARIMA.csv', row.names = FALSE)
