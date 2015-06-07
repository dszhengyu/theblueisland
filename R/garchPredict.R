
# parameter example
# arma = c(20, 3)
# predictDays = 30

library("rugarch")

# trainFileGARCH = 'z:\\theblueisland\\R\\trainFileGARCH.csv'
# predictFileGARCH = 'z:\\theblueisland\\R\\predictFileGARCH.csv'
# residualsFileGARCH = 'z:\\theblueisland\\R\\residualsFileGARCH.csv'

train <- read.csv('z:\\theblueisland\\R\\trainFileGARCH.csv', header = FALSE)

spec <-  ugarchspec(variance.model = list(model = "sGARCH", garchOrder = c(2, 2), submodel = NULL, 
                                          external.regressors = NULL, variance.targeting = TRUE), 
                    mean.model = list(armaOrder = arma, include.mean = FALSE, archm = FALSE, 
                                      archpow = 1, arfima = FALSE, external.regressors = NULL, archex = FALSE))
fit <- ugarchfit(spec, train)
predict <- ugarchforecast(fit, n.ahead = predictDays)
#plot(predict)
write.csv(fitted(predict), 'z:\\theblueisland\\R\\predictFileGARCH.csv', row.names = FALSE)
write.csv(residuals(fit), 'z:\\theblueisland\\R\\residualsFileGARCH.csv', row.names = FALSE)


