
# this script could test and predict, depend on the parameter 'online'
# online = 0

# global 
InputTimeLength = 6
OutputTimeLength = 1

library('nnet')
library(plyr)
library('AMORE')
#user_balance <- read.csv('z:\\theblueisland\\raw_data\\user_balance_table_parsed_date.csv')
user_balance_clean <- read.csv('z:\\theblueisland\\raw_data\\user_balance_table_clean.csv')
purchaseRedeemTotal <- ddply(user_balance_clean, c("report_date"), function(df)c(sum(df$total_purchase_amt), sum(df$total_redeem_amt)))
purchaseTotal <- purchaseRedeemTotal$V1
redeemTotal <- purchaseRedeemTotal$V2

# ############################### practice####################################################
# purchaseRedeemTotalTrain <- purchaseRedeemTotal[244 : 396, ]
# purchaseTotalTrain <- purchaseRedeemTotalTrain$V1
# timeVector <- purchaseTotalTrain
# XLength <- 30
# yLength <- 1
# 
# rowCount <- length(timeVector) - (XLength + yLength - 1)
# XIndex <- vector(length = rowCount * XLength)
# yIndex <- vector(length = rowCount * yLength)
# 
# XIndexSingle <- c(1 : XLength)
# yIndexSingle <- c((XLength + 1) : (XLength + yLength))
# for (i in 1 : rowCount) {
#   print (i)
#   from <- XLength * (i - 1) + 1
#   to <- XLength * i
#   fromY <- yLength * (i - 1) + 1
#   toY <- yLength * i
#   XIndex[from : to] <- XIndexSingle
#   yIndex[fromY : toY] <- yIndexSingle
#   XIndexSingle <- XIndexSingle + 1
#   yIndexSingle <- yIndexSingle + 1
# }
# 
# X <- data.frame(matrix(timeVector[XIndex], nrow <- rowCount,  nclos <- XLength, byrow <- TRUE))
# y <- data.frame(matrix(timeVector[yIndex], nrows <- rowCount, nclos <- yLength, byrow <- TRUE))
# XTest <- data.frame(matrix(timeVector[XIndexSingle], nrow <- 1,  nclos <- XLength, byrow <- TRUE))
###############################################practice end######################################

generateXy <- function(timeVector, XLength, yLength){
  rowCount <- length(timeVector) - (XLength + yLength - 1)
  XIndex <- vector(length = rowCount * XLength)
  yIndex <- vector(length = rowCount * yLength)
  
  XIndexSingle <- c(1 : XLength)
  yIndexSingle <- c((XLength + 1) : (XLength + yLength))
  for (i in 1 : rowCount) {
    from <- XLength * (i - 1) + 1
    to <- XLength * i
    fromY <- yLength * (i - 1) + 1
    toY <- yLength * i
    XIndex[from : to] <- XIndexSingle
    yIndex[fromY : toY] <- yIndexSingle
    XIndexSingle <- XIndexSingle + 1
    yIndexSingle <- yIndexSingle + 1
  }
  
  X <- data.frame(matrix(timeVector[XIndex], nrow <- rowCount,  nclos <- XLength, byrow <- TRUE))
  y <- data.frame(matrix(timeVector[yIndex], nrows <- rowCount, nclos <- yLength, byrow <- TRUE))
  XTest <- data.frame(matrix(timeVector[XIndexSingle], nrow <- 1,  nclos <- XLength, byrow <- TRUE))
  
  result <-list(X = X, y = y, XTest = XTest)
  return(result)
}

mean_squared_error <- function(yActual, ypredict) {
  return (sum((yActual - ypredict) * (yActual - ypredict)) / nrow(yActual))
}

scale01 <- function(X, max, min) {
  return ((X - min) / (max - min))
}

unscale01 <- function(X, max, min) {
  return (X * (max - min) + min)
}


if (online == 0) {
  
  # split train and test, split day is 20140801
  purchaseRedeemTotalTrain <- purchaseRedeemTotal[244 : 396, ]
  purchaseRedeemTotalTest <- purchaseRedeemTotal[397 : 427, ]
  
  ### purchase
  purchaseTotalTrain <- purchaseRedeemTotalTrain$V1
  purchaseTotalTest <- purchaseRedeemTotalTest$V1
  
  # extract X and y
  purchaseTotalTrainXy <- generateXy(purchaseTotalTrain, InputTimeLength, OutputTimeLength)
  X <- purchaseTotalTrainXy$X
  y <- purchaseTotalTrainXy$y
  XTest <- purchaseTotalTrainXy$XTest
  yTest <- matrix(purchaseTotalTest, ncol = OutputTimeLength)
  
  # set X , y and XTest to [0, 1]
  XMAX = sapply(X, max)
  XMin = sapply(X, min)
  XScaling <- t(apply(X, 1, scale01, XMAX, XMin))
  XTestScaling <- t(apply(XTest, 1, scale01, XMAX, XMin))
  yMAX = sapply(y, max)
  yMIN = sapply(y, min)
  yScaling <- sapply(y, scale01, yMAX, yMIN)
  
  # set ANN model and train
  purchaseModel <- nnet(XScaling, yScaling, size = 8, linout = TRUE)
  
#   purchasNet <- newff(n.neurons=c(InputTimeLength, 30, 15, OutputTimeLength), learning.rate.global=1e-3, 
#                momentum.global=0.01, error.criterium="LMS", Stao=NA, hidden.layer="tansig",
#                output.layer="purelin", method="ADAPTgdwm")
#   purchaseModel2 <- train(purchasNet, XScaling, yScaling,  error.criterium="LMS", report=TRUE, show.step=100, n.shows=5)
#   
  
  # test on train set, evaluate
  predictOnTrainScaling <- predict(purchaseModel, XScaling)
  predictOnTrain <- unscale01(predictOnTrainScaling, yMAX, yMIN)
  errorOnTrain = mean_squared_error(y, predictOnTrain)
  print ("errorOnTrain : ")
  print (errorOnTrain)
  
#   predictOnTrainScaling2 <- sim.MLPnet(purchaseModel2$net, XScaling)
#   predictOnTrain2 <- unscale01(predictOnTrainScaling2, yMAX, yMIN)
#   errorOnTrain2 = mean_squared_error(y, predictOnTrain2)
  
  plot(predictOnTrain, type = 'l', col = 'blue')
#   lines(predictOnTrain2, col = 'green')
  lines(y, col = 'red')
  
  # test on test set
  predictDays = 31
  XTestScaling <- c(XTestScaling[1,], 1 : predictDays)
  for (i in seq(from = 1, to = predictDays, by = OutputTimeLength)) {
    trainFrom <- i
    trainTo <- i + InputTimeLength - 1
    predictFrom <- InputTimeLength + i
    predictTo <- predictFrom + OutputTimeLength - 1
#     print (trainFrom)
#     print (trainTo)
#     print (predictFrom)
#     print (predictTo)
#     print ('\n')
    predictSingle <- predict(purchaseModel, XTestScaling[trainFrom : trainTo])
    XTestScaling[predictFrom : predictTo] = predictSingle[1]
  }
  predictFinalFrom <- InputTimeLength + 1
  predictFinalTo <- length(XTestScaling)
  predictOnTestScaling <- XTestScaling[predictFinalFrom : predictFinalTo]
  predictOnTestScaling <- matrix(predictOnTestScaling, ncol = OutputTimeLength)
  predictOnTest <- unscale01(predictOnTestScaling, yMAX, yMIN)
  errorOnTest <- mean_squared_error(yTest, predictOnTest)
  print ("errorOnTest : ")
  print (errorOnTest)
  
  plot(predictOnTest, type = 'l', col = 'blue')
  lines(yTest, col = 'red')
  
  # write predict on test set into file, need to re-evaluate on Python
  # or just write the mean_squared_error and errorVar

  
  ### redeem
  
  # extract X and y
  
  # set model and train
  
  # test on train set
  
  # test on test set
  
  # write predict on test set into file, need to re-evaluate on Python
  # or just write the mean_squared_error and errorVar
} else {
  # train using whole timeVector, extract X from it
  purchaseXyXTest <- generateXy(purchaseTotal, 15, 1)
  redeemXyXTest <- generateXy(redeemTotal, 15, 1)
  
  # predict using the latest XLength timeVector
  predictDays = 30

  # write predict into file
}