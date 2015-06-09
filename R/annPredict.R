
# this script could test and predict, depend on the parameter 'online'
# online = 0

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

mean_squared_error <- function(yActual, ypredict) {
  return (sum((yActual - ypredict) * (yActual - ypredict)) / nrow(yActual))
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

annTrainPredict <- function(timeVec, testVec, inputTimeLen, outPutTimelen, hiddenLayer, predictDays = 31) {
  timeVec <- purchaseTotalTrain
  testVec <- purchaseTotalTest
  inputTimeLen <- 1
  outPutTimelen <- 1
  hiddenLayer <- 16

  totalXyXTest <- generateXy(timeVec, inputTimeLen, outPutTimelen)
  X <- totalXyXTest$X
  y <- totalXyXTest$y
  XTest <- totalXyXTest$XTest
  yTest <- matrix(testVec, ncol = outPutTimelen)
  
  # set X , y and XTest to [0, 1]
  XMAX = sapply(X, max)
  XMin = sapply(X, min)
  # XScaling <- sapply(X, scale01, XMAX, XMin)
  XScaling <- data.frame((X - XMin)/(XMAX - XMin))
#   XTestScaling <- sapply(XTest, scale01, XMAX, XMin)
  XTestScaling <- data.frame((XTest - XMin)/(XMAX - XMin))
  yMAX = sapply(y, max)
  yMIN = sapply(y, min)
#   yScaling <- sapply(y, scale01, yMAX, yMIN)
  yScaling <- data.frame((y - yMIN)/(yMAX - yMIN))
  
#   print (XScaling)
#   print (yScaling)
  # set ANN model and train
  model <- nnet(XScaling, yScaling, size = hiddenLayer, linout = TRUE, trace = FALSE)
  
  # test on train set, evaluate
#   predictOnTrainScaling <- predict(model, XScaling)
#   predictOnTrain <- unscale01(predictOnTrainScaling, yMAX, yMIN)
#   errorOnTrain = mean_squared_error(y, predictOnTrain)
#   print ("errorOnTrain : ")
#   print (errorOnTrain)
#   plot(y, type = 'l', col = 'blue')
#   lines(predictOnTrain, col = 'red')
  
  # test on test set
  # predictDays = 31
  XTestScaling <- c(unlist(XTestScaling[1,]), 1 : predictDays)
  for (i in seq(from = 1, to = predictDays, by = outPutTimelen)) {
    trainFrom <- i
    trainTo <- i + inputTimeLen - 1
    predictFrom <- inputTimeLen + i
    predictTo <- predictFrom + outPutTimelen - 1
    #     print (trainFrom)
    #     print (trainTo)
    #     print (predictFrom)
    #     print (predictTo)
    #     print ('\n')
    predictSingle <- predict(model, XTestScaling[trainFrom : trainTo])
    XTestScaling[predictFrom : predictTo] = predictSingle[1]
  }
  predictFinalFrom <- inputTimeLen + 1
  predictFinalTo <- length(XTestScaling)
  predictOnTestScaling <- XTestScaling[predictFinalFrom : predictFinalTo]
  predictOnTestScaling <- matrix(predictOnTestScaling, ncol = outPutTimelen)
#   predictOnTest <- unscale01(predictOnTestScaling, yMAX, yMIN)
  predictOnTest <- (predictOnTestScaling * (yMAX - yMIN) + yMIN)
  testVec <- matrix(testVec, ncol = outPutTimelen)
  errorOnTest <- mean_squared_error(testVec, predictOnTest)
  errorVarOnTest <- error_variance(testVec, predictOnTest)
#   print ("errorOnTest : ")
#   print (errorOnTest)
#   plot(yTest, type = 'l', col = 'blue')
#   lines(predictOnTest, col = 'red')
  
  return (list(predict = predictOnTest, MSE = errorOnTest, errorVar = errorVarOnTest))
}

annGridSearch <- function(timeVec, testVec, inputTimeLengthMax, predictDays) {
  # tmp code below, use for debug
  # purchaseParam <- annGridSearch(purchaseTotalTrain, purchaseTotalTest, 10)
#   timeVec <- purchaseTotalTrain
#   testVec <- purchaseTotalTest
#   inputTimeLengthMax <- 10
#   predictDays <- 31

#   error <- vector(length = inputTimeLengthMax)
  errorVar <- vector(length = inputTimeLengthMax)
  index <- vector(length = inputTimeLengthMax)
  for (inputSingle in 1 : inputTimeLengthMax) {
    cat ("inputSingle = ", inputSingle, '\n')
    hiddenLayerMax <- as.integer(sqrt(inputSingle + 1) + 15)
#     errorSingle <- vector(length = hiddenLayerMax)
    errorVarSingle <- vector(length = hiddenLayerMax)
    for (hiddenSingle in 1 : hiddenLayerMax) {
      cat ("hiddenSingle = ", hiddenSingle, '\n')
      result <- annTrainPredict(timeVec, testVec, inputTimeLengthMax, outPutTimelen = 1, hiddenSingle, predictDays)
#       MSESingle <- result$MSE
      errorVarSingleValue <- result$errorVar
#       errorSingle[hiddenSingle] <- MSESingle
      errorVarSingle[hiddenSingle] <- errorVarSingleValue
#       print (MSESingle)
#       print ("****************************************************************")
    }
    errorVar[inputSingle] <- min(errorVarSingle)
    index[inputSingle] <- which.min(errorVarSingle)
  }
  optimalInput <- which.min(errorVar)
  optimalHidden <- index[optimalInput]
  minErrorVar <- errorVar[optimalInput]
  result <- annTrainPredict(timeVec, testVec, optimalInput, outPutTimelen = 1, optimalHidden, predictDays)
  predict <- result$predict
  plot(testVec, type = 'l', main = 'GridSearchResult', col = 'red')
  lines(predict, col = 'blue')
  cat ("optimalInput = ", optimalInput, '\n')
  cat ("optimalHidden = ", optimalHidden, '\n')
#   print ("predict = ")
#   print (predict)
  finalErrorVar <- result$errorVar
  cat ("finalErrorVar = ", finalErrorVar, '\n')
  return (list(input = optimalInput, hidden = optimalHidden, predict = predict, finalErrorVar = finalErrorVar))
}

annEnsembleLocal <- function(timeVec, testVec, inputTimeLengthMax, modelCount = 3, predictDays = 31)
{
#   timeVec <- purchaseTotalTrain
#   testVec <- purchaseTotalTest
#   inputTimeLengthMax <- 10
#   modelCount = 3
#   predictDays = 31
  
  errorVar <- vector(length = modelCount)
  weight <- vector(length = modelCount)
  predict <- matrix(0, nrow = predictDays, ncol = modelCount)
  for (i in 1 : modelCount) {
#     cat("i = ", i, '\n')
    result <- annGridSearch(timeVec, testVec, inputTimeLengthMax, predictDays)
    predict[, i] <- result$predict
    errorVar[i] <- result$finalErrorVar
  }
  errorVarSum <- sum(errorVar)
  weight <- ((errorVarSum - errorVar) / errorVarSum) / (modelCount - 1)
  predictFinal <- matrix(0, nrow = predictDays)
  for (i in 1 : modelCount)  
    predictFinal <-  predictFinal + predict[, i] * weight[i]
  plot(testVec, type = 'l', col = 'red', main = 'Purchase-Ensemble')
  lines(predictFinal, col = 'blue')
  testVec <- matrix(testVec, ncol = 1)
  errorLocal <- mean_squared_error(testVec, predictFinal)
  cat ("errorLocal : ", errorLocal, '\n')
  errorvarLocal <- error_variance(testVec, predictFinal)
  cat ("errorvarLocal : ", errorvarLocal, '\n')
}

################################################ subroutine up there ################################

library('nnet')
library(plyr)
library('AMORE')
# user_balance <- read.csv('z:\\theblueisland\\raw_data\\user_balance_table_parsed_date.csv')
# user_balance_clean <- read.csv('z:\\theblueisland\\raw_data\\user_balance_table_clean.csv')
# purchaseRedeemTotal <- ddply(user_balance_clean, c("report_date"), function(df)c(sum(df$total_purchase_amt), sum(df$total_redeem_amt)))
# write.csv(purchaseRedeemTotal, 'z:\\theblueisland\\R\\purchaseRedeemTotal.csv', row.names = FALSE)
purchaseRedeemTotal <- read.csv('z:\\theblueisland\\R\\purchaseRedeemTotal.csv')
purchaseTotal <- purchaseRedeemTotal$V1
redeemTotal <- purchaseRedeemTotal$V2

if (online == 0) {
  
  # split train and test, split day is 20140801
  purchaseRedeemTotalTrain <- purchaseRedeemTotal[124 : 396, ]
  purchaseRedeemTotalTest <- purchaseRedeemTotal[397 : 427, ]
  
  ################# purchase###################################
  purchaseTotalTrain <- purchaseRedeemTotalTrain$V1
  purchaseTotalTest <- purchaseRedeemTotalTest$V1
  
  purchaseParam <- annGridSearch(purchaseTotalTrain, purchaseTotalTest, 10)
  purchaseInputTimeLength = purchaseParam$input
  purchaseHiddenLayer = purchaseParam$hidden
  
#   purchaseInputTimeLength = 6
#   hiddenLayer = 9
  purchaseResult <- annTrainPredict(purchaseTotalTrain, purchaseTotalTest, purchaseInputTimeLength, 1, purchaseHiddenLayer)
  
  purchasePredict <- purchaseResult$predict
  plot(purchasePredict, type = 'l', main = 'Purchase', col = 'green')
  lines(purchaseTotalTest, col = 'red')
  
  # write predict on test set into file, need to re-evaluate on Python
  # or just write the mean_squared_error and errorVar

  
  ############### redeem #########################################
  redeemTotalTrain <- purchaseRedeemTotalTrain$V2
  redeemTotalTest <- purchaseRedeemTotalTest$V2
 
  redeemParam <- annGridSearch(redeemTotalTrain, redeemTotalTest, 30)
  redeemInputTimeLength = redeemParam$input
  redeemHiddenLayer = redeemParam$hidden
  
  #   redeemInputTimeLength = 6
  #   redeemHiddenLayer = 9
  redeemResult <- annTrainPredict(redeemTotalTrain, redeemTotalTest, redeemInputTimeLength, 1, redeemHiddenLayer)
  
  redeemPredict <- redeemResult$predict
  plot(redeemPredict, type = 'l', main = 'Redeem', col = 'green')
  lines(redeemTotalTest, col = 'red')
  
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