
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

annTrainPredict <- function(timeVec, testVec, wholeVec, interestVec, interestOnline, inputTimeLen, outPutTimelen, hiddenLayer, predictDays = 31, online = 0) {
#   timeVec <- purchaseTotalTrain
#   testVec <- purchaseTotalCV
#   wholeVec <- purchaseTotalWhole
#   interestVec <- interestTrainCV
#   inputTimeLen <- 3
#   outPutTimelen <- 1
#   hiddenLayer <- 16
#   predictDays <- 31
#   online <- 1

  totalXyXTest <- generateXy(timeVec, inputTimeLen, outPutTimelen)
  X <- totalXyXTest$X
  y <- totalXyXTest$y
  XTest <- totalXyXTest$XTest
  yTest <- matrix(testVec, ncol = outPutTimelen)
  
  
  interestSingle <- interestVec[, 2]
  
  interestSingleTotal <- generateXy(interestSingle, inputTimeLen, outPutTimelen)$X
  interest4Train <- interestSingleTotal[0 : dim(X)[1], , drop = FALSE]
  interest4Test <- interestSingleTotal[(dim(X)[1] + 1) : (dim(interestSingleTotal)[1]), , drop = FALSE]
  rownames(interest4Test) <- 1:nrow(interest4Test)
  
  interest4TrainTotal <- interest4Train
  interest4TestTotal <- interest4Test
  
  X <- cbind(X, interest4TrainTotal)
  
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
  
  InterestMax <- sapply(interest4TestTotal, max)
  InterestMin <- sapply(interest4TestTotal, min)
  interest4TestTotalScaling <- data.frame((interest4TestTotal - InterestMin) / (InterestMax - InterestMin))
  
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
    xSingleDataframe <- data.frame(matrix(XTestScaling[trainFrom : trainTo], ncol = inputTimeLen))
    interestSingleDataframe <- data.frame(matrix(interest4TestTotalScaling[i, ], ncol = inputTimeLen))
    xSingle <- cbind(xSingleDataframe, interestSingleDataframe)
    predictSingle <- predict(model, xSingle)
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

  predictOnline <- 0
  if (online == 1) {
    result <- annTrainPredict(wholeVec, testVec[1 : 30], 0, interestOnline, 0, inputTimeLen, outPutTimelen, hiddenLayer, predictDays = 30, online = 0)
    predictOnline <- result$predict
  }
  
  return (list(predict = predictOnTest, MSE = errorOnTest, errorVar = errorVarOnTest, predictOnline = predictOnline))
}

annGridSearch <- function(timeVec, cvVec, testVec, wholeVec, interestWholeVec, inputTimeLengthMax, predictDays) {
  # tmp code below, use for debug
  # purchaseParam <- annGridSearch(purchaseTotalTrain, purchaseTotalTest, 10)
#   timeVec <- purchaseTotalTrain
#   cvVec <- purchaseTotalCV
#   testVec <- purchaseTotalTest
#   wholeVec <- purchaseTotalWhole
#   interestWholeVec <- interestTotalWhole
#   inputTimeLengthMax <- 10
#   predictDays <- 31
  
  interestTrainCV <- interestWholeVec[0 : (dim(interestWholeVec)[1] - 31 - 30), ]
  interestTrainTest <- interestWholeVec[0 : (dim(interestWholeVec)[1] - 30), ]
  interestOnline <- interestWholeVec
  ##### Cross-validation or not ###########
  trainSet <- c(timeVec, cvVec)
  
#   error <- vector(length = inputTimeLengthMax)
  errorVar <- vector(length = inputTimeLengthMax)
  index <- vector(length = inputTimeLengthMax)
  for (inputSingle in 1 : inputTimeLengthMax) {
#     cat ('\n', "inputSingle = ", inputSingle, '\n')
    hiddenLayerMax <- as.integer(sqrt(inputSingle + 1) + 13)
#     errorSingle <- vector(length = hiddenLayerMax)
    errorVarSingle <- vector(length = hiddenLayerMax)
    for (hiddenSingle in 1 : hiddenLayerMax) {
#       cat ("hiddenSingle = ", hiddenSingle, '\n')
      result <- annTrainPredict(trainSet, testVec, wholeVec, interestTrainTest, interestOnline,
                                inputTimeLengthMax, outPutTimelen = 1, hiddenSingle, predictDays)
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
  # use test
  trainSet <- c(timeVec, cvVec)
  result <- annTrainPredict(trainSet, testVec, wholeVec, interestTrainTest, interestOnline, optimalInput, outPutTimelen = 1, 
                            optimalHidden, predictDays, online = 1)
  predict <- result$predict
  plot(cvVec, type = 'l', main = 'GridSearchResult', col = 'red')
  lines(predict, col = 'blue')
  cat ("optimalInput = ", optimalInput, '\n')
  cat ("optimalHidden = ", optimalHidden, '\n')
#   print ("predict = ")
#   print (predict)
  finalErrorVar <- result$errorVar
  cat ("finalErrorVar = ", finalErrorVar, '\n')
  onlineSet <- result$predictOnline
  plot(onlineSet, type = 'l', main = 'Online', col = 'orange')
  
  return (list(input = optimalInput, hidden = optimalHidden, predict = predict, 
               finalErrorVar = finalErrorVar, onlineSet = onlineSet))
}

annEnsemble <- function(timeVec, cvVec, testVec, wholeVec, interestWholeVec, inputTimeLengthMax, modelCount = 3, predictDays = 31)
{
#   timeVec <- purchaseTotalTrain
#   cvVec <- purchaseTotalCV
#   testVec <- purchaseTotalTest
#   wholeVec <- purchaseTotalWhole
#   interestWholeVec <- interestTotalWhole
#   inputTimeLengthMax <- 20
#   modelCount = 5
#   predictDays = 31
  
  errorVar <- vector(length = modelCount)
  weight <- vector(length = modelCount)
  predict <- matrix(0, nrow = predictDays, ncol = modelCount)
  online <- matrix(0, nrow = 30, ncol = modelCount)
  for (i in 1 : modelCount) {
    cat('\n', "*********** In model ", i, '********************\n')
    result <- annGridSearch(timeVec, cvVec, testVec, wholeVec, interestWholeVec, inputTimeLengthMax, predictDays)
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
  plot(testVec, type = 'l', col = 'red', main = 'Local-Ensemble')
  lines(predictFinal, col = 'blue')
  testVec <- matrix(testVec, ncol = 1)
  errorLocal <- mean_squared_error(testVec, predictFinal)
  cat('\n', '%%%%%%%%%%%%%%%%%%%%%%%%%% Final &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&', '\n')
  cat ("errorLocal : ", errorLocal, '\n')
  errorvarLocal <- error_variance(testVec, predictFinal)
  cat ("errorvarLocal : ", errorvarLocal, '\n')
  plot(onlineFinal, type = 'l', col = 'orange', main = 'Online-Ensemble')
  
  return (list(localPredict = predictFinal, onlinePredict = onlineFinal))
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
interestTotal <- read.csv('z:\\theblueisland\\raw_data\\Interest_total.csv')
purchaseTotal <- purchaseRedeemTotal$V1
redeemTotal <- purchaseRedeemTotal$V2

# split train and test, split day is 20140801
startDate <- 244
train_cv_date <- 366
cv_test_date <- 397
end_date <- 427
purchaseRedeemTotalTrain <- purchaseRedeemTotal[startDate : (train_cv_date - 1), ]
purchaseRedeemTotalCV <- purchaseRedeemTotal[train_cv_date : (cv_test_date - 1), ]
purchaseRedeemTotalTest <- purchaseRedeemTotal[cv_test_date : end_date, ]
purchaseRedeemTotalWhole <- purchaseRedeemTotal[startDate : end_date, ]

# split interest
interestTotalWhole <- interestTotal[startDate : dim(interestTotal)[1], ]

################# purchase############################################################
purchaseTotalTrain <- purchaseRedeemTotalTrain$V1
purchaseTotalCV <- purchaseRedeemTotalCV$V1
purchaseTotalTest <- purchaseRedeemTotalTest$V1
purchaseTotalWhole <- purchaseRedeemTotalWhole$V1

cat('\n', '@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Purchase &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&', '\n')
purchaseResult <- annEnsemble(purchaseTotalTrain, purchaseTotalCV, purchaseTotalTest, purchaseTotalWhole,
                              interestTotalWhole, inputTimeLengthMax = 23, modelCount = 6, predictDays = 31)

purchaseOnline <- purchaseResult$onlinePredict

############### redeem #########################################
redeemTotalTrain <- purchaseRedeemTotalTrain$V2
redeemTotalCV <- purchaseRedeemTotalCV$V2
redeemTotalTest <- purchaseRedeemTotalTest$V2
redeemTotalWhole <- purchaseRedeemTotalWhole$V2

cat('\n', '@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Redeem &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&', '\n')
redeemResult <- annEnsemble(redeemTotalTrain, redeemTotalCV, redeemTotalTest, redeemTotalWhole, 
                            interestTotalWhole, inputTimeLengthMax = 23, modelCount = 6, predictDays = 31)

redeemOnline <- redeemResult$onlinePredict

########$$$$$$$$$$$$$$$$$$$$$ merge online set $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$########
# purchaseOnline
# redeemOnline

startDate <- as.Date('2014-09-01')
dateSeries <- vector(length = 30)
for (i in 1 : 30) {
  dateSeries[i] <- as.numeric(strftime(startDate, format = '%Y%m%d'))
  startDate <- startDate + 1
}
online <- data.frame(dateSeries, purchaseOnline, redeemOnline)
write.table(x = online, file = 'z:\\theblueisland\\R\\tc_comp_predict_table.csv', 
            row.names = FALSE, col.names = FALSE, sep = ',')

