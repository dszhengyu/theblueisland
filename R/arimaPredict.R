#orderUsed = c(8, 1, 8)
#predictDays = 30

library('stats')
train <- read.csv('z:\\theblueisland\\R\\trainFile.csv', header = FALSE)
model <-arima(train, order = orderUsed)
pre = predict(model, predictDays)
write.csv(pre[["pred"]], 'z:\\theblueisland\\R\\predictFile.csv', row.names = FALSE)
write.csv(residuals(model), 'z:\\theblueisland\\R\\residualsFile.csv', row.names = FALSE)


#model2 = Arima(train, order = c(8, 1, 8))
#pre2 = forecast(model2, h = 30)
