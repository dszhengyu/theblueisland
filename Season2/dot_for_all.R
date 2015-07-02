run_online = F

generateXy <- function(timeVector, XLength, yLength){
  #   timeVector <- purchaseTotalTrain
  #   XLength <- 1
  #   yLength <- 1
  
  rowCount <- length(timeVector) - (XLength + yLength - 1)
  XIndex <- vector(length = (rowCount * XLength))
  yIndex <- vector(length = (rowCount * yLength))
  
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

mean_squared_error <- function(yActual, yPredict) {
  return (sum((yActual - yPredict) * (yActual - yPredict)) / nrow(yActual))
}

error_variance <- function(yActual, yPredict) {
  return (var(abs((yActual - yPredict)) / yActual))
}

calculateDistance <- function(X, xNew) {
  return (sqrt(rowSums(t((t(X) - xNew) * (t(X) - xNew)))))
}

singleDotPredict <- function(X, y, xNew, trainCount = 20) {
#   X <- XScaling
#   y <- yScaling
#   xNew <- XTestScaling[1 : 1]
#   trainCount = 20
  
  distance <- calculateDistance(X, xNew)
  trainIndex <- order(distance)[1 : trainCount]
  XTrain <- X[trainIndex, , drop = FALSE]
  yTrain <- y[trainIndex, , drop = FALSE]
  
#   # plot the choosen lines
#   plot((1 : ncol(XTrain)), xNew, type = 'l', col = 'red')
#   for (lineIndex in trainIndex) {
#     #print(lineIndex)
#     lines((1 : ncol(XTrain)), XTrain[toString(lineIndex), ])
#   }
  
  # fit lm model
  fit <- glmnet(as.matrix(XTrain), yTrain[ , 1])
  predict <- predict(fit, newx = matrix(xNew, nrow = 1), s=c(0.01))
  
  return (predict[1])
}

dotPredict <- function(timeVec, testVec, wholeVec, window, step = 1, predictDays = 31, online = 0) {
#   timeVec <- purchaseTotalTrain
#   testVec <- purchaseTotalTest
#   wholeVec <- purchaseTotalWhole
#   window <- 1
#   step = 1
#   predictDays = 31
#   online = 1
  
  totalXyXTest <- generateXy(timeVec, window, step)
  X <- totalXyXTest$X
  y <- totalXyXTest$y
  XTest <- totalXyXTest$XTest
  yTest <- matrix(testVec, ncol = step)
  
  # scaling to [0, 1]
  XMAX = sapply(X, max)
  XMin = sapply(X, min)
  XScaling <- data.frame((X - XMin)/(XMAX - XMin))
  XTestScaling <- data.frame((XTest - XMin)/(XMAX - XMin))
  yMAX = sapply(y, max)
  yMIN = sapply(y, min)
  yScaling <- data.frame((y - yMIN)/(yMAX - yMIN))
  
  # start predict
  XTestScaling <- c(unlist(XTestScaling[1,]), 1 : predictDays)
  for (i in seq(from = 1, to = predictDays, by = step)) {
    trainFrom <- i
    trainTo <- i + window - 1
    predictFrom <- window + i
    predictTo <- predictFrom + step - 1
    xSingle <- XTestScaling[trainFrom : trainTo]
#     print (trainFrom)
#     print (trainTo)
#     print (xSingle)
    predictSingle <- singleDotPredict(XScaling, yScaling, xSingle, trainCount = 20)
    XTestScaling[predictFrom : predictTo] = predictSingle
  }
  predictFinalFrom <- window + 1
  predictFinalTo <- length(XTestScaling)
  predictOnTestScaling <- XTestScaling[predictFinalFrom : predictFinalTo]
  predictOnTestScaling <- matrix(predictOnTestScaling, ncol = step)
  predictOnTest <- (predictOnTestScaling * (yMAX - yMIN) + yMIN)
  
  testVec <- matrix(testVec, ncol = step)
  errorOnTest <- mean_squared_error(testVec, predictOnTest)
  errorVarOnTest <- error_variance(testVec, predictOnTest)
  
  # predict online
  predictOnline <- 0
  if (online == 1) {
    result <- dotPredict(wholeVec, testVec[1 : 30], 0, window, step, predictDays = 30, online = 0)
    predictOnline <- result$predict
  }
  
  return (list(predict = predictOnTest, MSE = errorOnTest, 
               errorVar = errorVarOnTest, predictOnline = predictOnline))
}

dotPredictGridSearch <- function(timeVec, testVec, wholeVec, windowMax, predictDays = 31) {
#   timeVec <- purchaseTotalTrain
#   testVec <- purchaseTotalTest
#   wholeVec <- purchaseTotalWhole
#   windowMax <- 5
#   predictDays = 31
  
  errorVar <- vector(length = windowMax)
  errorVar[1] <- 1.0e+20
  for (windowSingle in 2 : windowMax) {
    cat("windowSingle = ", windowSingle, '\n')
    result <- dotPredict(timeVec, testVec, wholeVec, windowSingle, 
                         step = 1, predictDays, online = 0)
    MSESingle <- result$MSE
    errorVar[windowSingle] <- MSESingle
    cat("MSE = ", MSESingle, '\n')
    print("****************************************************************")
  }
  
  optimalWindow <- which.min(errorVar)
  cat("optimalWindow = ", optimalWindow, '\n')
  minErrorVar <- errorVar[optimalWindow]

  # predict with optimal Window
  result <- dotPredict(timeVec, testVec, wholeVec, optimalWindow, 
                       step = 1, predictDays, online = 1)
  predict <- result$predict
  plot(testVec, type = 'l', main = 'GridSearchResult', col = 'red')
  lines(predict, col = 'blue')

  finalErrorVar <- result$errorVar
  cat("finalErrorVar = ", finalErrorVar, '\n')
  onlineSet <- result$predictOnline
  plot(onlineSet, type = 'l', main = 'Online', col = 'orange')
  
  return (list(window = optimalWindow, predict = predict, 
               finalErrorVar = finalErrorVar, onlineSet = onlineSet))
}

################################################ subroutine up there ################################
# impport library
library('glmnet')

if (run_online == F) {
  purchaseRedeemTotal <- read.csv('z:\\theblueisland\\Season2\\daily_purchase_redeem.csv')
} else {
  purchaseRedeemTotal <- dataset1
}

purchaseTotal <- purchaseRedeemTotal$purchase
redeemTotal <- purchaseRedeemTotal$redeem

start_date <- 244
test_date <- 397
end_date <- 427
purchaseRedeemTotalTrain <- purchaseRedeemTotal[start_date : (test_date - 1), ]
purchaseRedeemTotalTest <- purchaseRedeemTotal[test_date : end_date, ]
purchaseRedeemTotalWhole <- purchaseRedeemTotal[start_date : end_date, ]

################# purchase#####################################
purchaseTotalTrain <- purchaseRedeemTotalTrain$purchase
purchaseTotalTest <- purchaseRedeemTotalTest$purchase
purchaseTotalWhole <- purchaseRedeemTotalWhole$purchase

cat('\n', '@@@@@@@@@@@@@@@@@@@ Purchase &&&&&&&&&&&&&&&&&&&&&&', '\n')
purchaseResult <- dotPredictGridSearch(purchaseTotalTrain, 
                                       purchaseTotalTest, 
                                       purchaseTotalWhole,
                                       windowMax = 50)
purchaseOnline <- purchaseResult$onlineSet

############### redeem #########################################
redeemTotalTrain <- purchaseRedeemTotalTrain$redeem
redeemTotalTest <- purchaseRedeemTotalTest$redeem
redeemTotalWhole <- purchaseRedeemTotalWhole$redeem

cat('\n', '@@@@@@@@@@@@@@@@@@@@ Redeem &&&&&&&&&&&&&&&&&&&&&&&&', '\n')
redeemResult <- dotPredictGridSearch(redeemTotalTrain, 
                                     redeemTotalTest, 
                                     redeemTotalWhole,
                                     windowMax = 50)

redeemOnline <- redeemResult$onlineSet

########$$$$$$$$$$$$$$$$$$$$$ merge online set $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$########
startDate <- as.Date('2014-09-01')
dateSeries <- vector(length = 30)
for (i in 1 : 30) {
  dateSeries[i] <- as.numeric(strftime(startDate, format = '%Y%m%d'))
  startDate <- startDate + 1
}
online <- data.frame(dateSeries, purchaseOnline, redeemOnline)

if (run_online == F) {
  write.table(x = online, file = 'z:\\theblueisland\\Season2\\online_dot_for_all.csv', row.names = FALSE, col.names = FALSE, sep = ',')
}

dataname <- online

