run_online = F

generateXy <- function(timeVector, XLength, yLength){
  
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

scale01 <- function(X, max, min) {
  return ((X - min) / (max - min))
}

unscale01 <- function(X, max, min) {
  return (X * (max - min) + min)
}

annTrainPredict <- function(timeVec, testVec, wholeVec, inputTimeLen, 
                            outPutTimelen, hiddenLayer, predictDays = 31, online = 0) {
  
  totalXyXTest <- generateXy(timeVec, inputTimeLen, outPutTimelen)
  X <- totalXyXTest$X
  y <- totalXyXTest$y
  XTest <- totalXyXTest$XTest
  yTest <- matrix(testVec, ncol = outPutTimelen)
  
  XMAX = sapply(X, max)
  XMin = sapply(X, min)
  XScaling <- data.frame((X - XMin)/(XMAX - XMin))
  XTestScaling <- data.frame((XTest - XMin)/(XMAX - XMin))
  yMAX = sapply(y, max)
  yMIN = sapply(y, min)
  yScaling <- data.frame((y - yMIN)/(yMAX - yMIN))
 
  model <- nnet(XScaling, yScaling, size = hiddenLayer, linout = TRUE, trace = FALSE)
  
  
  XTestScaling <- c(unlist(XTestScaling[1,]), 1 : predictDays)
  for (i in seq(from = 1, to = predictDays, by = outPutTimelen)) {
    trainFrom <- i
    trainTo <- i + inputTimeLen - 1
    predictFrom <- inputTimeLen + i
    predictTo <- predictFrom + outPutTimelen - 1
    xSingle <- data.frame(matrix(XTestScaling[trainFrom : trainTo], ncol = inputTimeLen))
    predictSingle <- predict(model, xSingle)
    XTestScaling[predictFrom : predictTo] = predictSingle[1]
  }
  predictFinalFrom <- inputTimeLen + 1
  predictFinalTo <- length(XTestScaling)
  predictOnTestScaling <- XTestScaling[predictFinalFrom : predictFinalTo]
  predictOnTestScaling <- matrix(predictOnTestScaling, ncol = outPutTimelen)
  predictOnTest <- (predictOnTestScaling * (yMAX - yMIN) + yMIN)
  
  testVec <- matrix(testVec, ncol = outPutTimelen)
  errorOnTest <- mean_squared_error(testVec, predictOnTest)
  errorVarOnTest <- error_variance(testVec, predictOnTest)
  
  predictOnline <- 0
  if (online == 1) {
    result <- annTrainPredict(wholeVec, testVec[1 : 30], 0, inputTimeLen, 
                              outPutTimelen, hiddenLayer, predictDays = 30, online = 0)
    predictOnline <- result$predict
  }
  
  return (list(predict = predictOnTest, MSE = errorOnTest, 
               errorVar = errorVarOnTest, predictOnline = predictOnline))
}

annGridSearch <- function(timeVec, cvVec, testVec, wholeVec, inputTimeLengthMax, predictDays) {
  
  trainSet <- c(timeVec, cvVec)
  
  errorVar <- vector(length = inputTimeLengthMax)
  index <- vector(length = inputTimeLengthMax)
  for (inputSingle in 1 : inputTimeLengthMax) {
    hiddenLayerMax <- as.integer(sqrt(inputSingle + 1) + 13)
    errorVarSingle <- vector(length = hiddenLayerMax)
    for (hiddenSingle in 1 : hiddenLayerMax) {
      result <- annTrainPredict(trainSet, testVec, wholeVec, inputTimeLengthMax, 
                                outPutTimelen = 1, hiddenSingle, predictDays)
      errorVarSingleValue <- result$errorVar
      errorVarSingle[hiddenSingle] <- errorVarSingleValue
    }
    errorVar[inputSingle] <- min(errorVarSingle)
    index[inputSingle] <- which.min(errorVarSingle)
  }
  optimalInput <- which.min(errorVar)
  optimalHidden <- index[optimalInput]
  minErrorVar <- errorVar[optimalInput]
  trainSet <- c(timeVec, cvVec)
  result <- annTrainPredict(trainSet, testVec, wholeVec, optimalInput, outPutTimelen = 1, 
                            optimalHidden, predictDays, online = 1)
  predict <- result$predict
  finalErrorVar <- result$errorVar
  onlineSet <- result$predictOnline
  
  return (list(input = optimalInput, hidden = optimalHidden, predict = predict, 
               finalErrorVar = finalErrorVar, onlineSet = onlineSet))
}

annEnsemble <- function(timeVec, cvVec, testVec, wholeVec, inputTimeLengthMax, 
                        modelCount = 3, predictDays = 31)
{
  
  errorVar <- vector(length = modelCount)
  weight <- vector(length = modelCount)
  predict <- matrix(0, nrow = predictDays, ncol = modelCount)
  online <- matrix(0, nrow = 30, ncol = modelCount)
  for (i in 1 : modelCount) {
    result <- annGridSearch(timeVec, cvVec, testVec, wholeVec, inputTimeLengthMax, predictDays)
    errorVar[i] <- result$finalErrorVar
    predict[, i] <- result$predict
    online[, i] <- result$onlineSet
  }
  errorVarSum <- sum(errorVar)
  weight <- ((errorVarSum - errorVar) / errorVarSum) / (modelCount - 1)
  predictFinal <- matrix(0, nrow = predictDays)
  onlineFinal <- matrix(0, nrow = 30)
  for (i in 1 : modelCount) {
    predictFinal <-  predictFinal + predict[, i] * weight[i]
    onlineFinal <- onlineFinal + online[, i] * weight[i]
  }
  testVec <- matrix(testVec, ncol = 1)
  errorLocal <- mean_squared_error(testVec, predictFinal)
  errorvarLocal <- error_variance(testVec, predictFinal)
  
  return (list(localPredict = predictFinal, onlinePredict = onlineFinal))
}


library('nnet')

if (run_online == F) {
  purchaseRedeemTotal <- read.csv('z:\\theblueisland\\Season2\\daily_purchase_redeem.csv')
} else {
  purchaseRedeemTotal <- dataset1
}

purchaseTotal <- purchaseRedeemTotal$purchase
redeemTotal <- purchaseRedeemTotal$redeem
startDate <- 244
train_cv_date <- 366
cv_test_date <- 397
end_date <- 427
purchaseRedeemTotalTrain <- purchaseRedeemTotal[startDate : (train_cv_date - 1), ]
purchaseRedeemTotalCV <- purchaseRedeemTotal[train_cv_date : (cv_test_date - 1), ]
purchaseRedeemTotalTest <- purchaseRedeemTotal[cv_test_date : end_date, ]
purchaseRedeemTotalWhole <- purchaseRedeemTotal[startDate : end_date, ]

purchaseTotalTrain <- purchaseRedeemTotalTrain$purchase
purchaseTotalCV <- purchaseRedeemTotalCV$purchase
purchaseTotalTest <- purchaseRedeemTotalTest$purchase
purchaseTotalWhole <- purchaseRedeemTotalWhole$purchase

purchaseResult <- annEnsemble(purchaseTotalTrain, purchaseTotalCV, purchaseTotalTest, purchaseTotalWhole,
                              inputTimeLengthMax = 23, modelCount = 6, predictDays = 31)

purchaseOnline <- purchaseResult$onlinePredict

redeemTotalTrain <- purchaseRedeemTotalTrain$redeem
redeemTotalCV <- purchaseRedeemTotalCV$redeem
redeemTotalTest <- purchaseRedeemTotalTest$redeem
redeemTotalWhole <- purchaseRedeemTotalWhole$redeem

redeemResult <- annEnsemble(redeemTotalTrain, redeemTotalCV, redeemTotalTest, redeemTotalWhole, 
                            inputTimeLengthMax = 23, modelCount = 6, predictDays = 31)

redeemOnline <- redeemResult$onlinePredict

startDate <- as.Date('2014-09-01')
dateSeries <- vector(length = 30)
for (i in 1 : 30) {
  dateSeries[i] <- as.numeric(strftime(startDate, format = '%Y%m%d'))
  startDate <- startDate + 1
}
online <- data.frame(dateSeries, purchaseOnline, redeemOnline)

if (run_online == F) {
  write.table(x = online, file = 'z:\\theblueisland\\Season2\\tc_comp_predict_table.csv', row.names = FALSE, col.names = FALSE, sep = ',')
}

dataname <- online