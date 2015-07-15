run_online = FALSE

addWeekdayFeature <- function(X) {
  # X <- purchaseTotalWhole
  
  rowNumber <- (1 : nrow(X))
  rowNumber <- rowNumber %% 7  
  weekDay <- matrix(nrow = nrow(X), ncol = 7)
  for (i in (1 : 7)) {
    weekDay[ , i] <- (rowNumber == (i - 1))
  }
  binaryFeature <- matrix(data = sapply(weekDay, as.integer), nrow = nrow(X), ncol = 7)
  return (cbind(X, binaryFeature))
}

################################################ subroutine up there ################################

if (run_online == F) {
  purchaseRedeemTotal <- read.csv('z:\\theblueisland\\Season2\\daily_purchase_redeem.csv')
} else {
  purchaseRedeemTotal <- dataset1
}

purchaseRedeemTotal <- addWeekdayFeature(purchaseRedeemTotal)
weekdayFeature <- purchaseRedeemTotal[, 4 : 10]

start_date <- 275
test_date <- 397
end_date <- 427
purchaseRedeemTotalTrain <- purchaseRedeemTotal[start_date : (test_date - 1), ]
purchaseRedeemTotalTest <- purchaseRedeemTotal[test_date : end_date, ]
purchaseRedeemTotalWhole <- purchaseRedeemTotal[start_date : end_date, ]

################# purchase #####################################
purchaseTotalTrain <- purchaseRedeemTotalTrain[ , c(2, 4 : 10)]
purchaseTotalTest <- purchaseRedeemTotalTest[ , c(2, 4 : 10)]
purchaseTotalWhole <- purchaseRedeemTotalWhole[ , c(2, 4 : 10)]

from <- 428
fromIndex <- from %% 7 + 7
toIndex <- fromIndex + 29
onlineFeature <- weekdayFeature[fromIndex : toIndex, ]
colnames(onlineFeature) <- c("monday", "tuesday", "wednesday", 
                             "thursday", "friday", "saturday", "sunday")

purchaseTrain <- purchaseTotalWhole
colnames(purchaseTrain) <- c("purchase", "monday", "tuesday", "wednesday", 
                     "thursday", "friday", "saturday", "sunday")
formulaStr <- "purchase~ monday + tuesday + wednesday + thursday + friday + saturday + sunday"
model = lm(as.formula(formulaStr), purchaseTrain)
purchaseOnline <- data.frame(predict(model, onlineFeature, level=0.95,se.fit=FALSE))

################# redeem #####################################
redeemTotalTrain <- purchaseRedeemTotalTrain[ , c(3, 4 : 10)]
redeemTotalTest <- purchaseRedeemTotalTest[ , c(3, 4 : 10)]
redeemTotalWhole <- purchaseRedeemTotalWhole[ , c(3, 4 : 10)]

redeemTrain <- redeemTotalWhole
colnames(redeemTrain) <- c("redeem", "monday", "tuesday", "wednesday", 
                     "thursday", "friday", "saturday", "sunday")
formulaStr <- "redeem~ monday + tuesday + wednesday + thursday + friday + saturday + sunday"
model = lm(as.formula(formulaStr), redeemTrain)
redeemOnline <- data.frame(predict(model, onlineFeature, level=0.95,se.fit=FALSE))

########$$$$$$$$$$$$$$$$$$$$$ local online set $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$########
startDate <- as.Date('2014-09-01')
report_date <- vector(length = 30)
for (i in 1 : 30) {
  report_date[i] <- as.numeric(strftime(startDate, format = '%Y%m%d'))
  startDate <- startDate + 1
}
online <- data.frame(report_date, purchaseOnline, redeemOnline)
row.names(online) <- (1 : 30)

colnames(online) <- c("report_date", "purchaseOnline", "redeemOnline")
if (run_online == F) {
  write.table(x = online, file = 'z:\\theblueisland\\Season2\\online_baseline.csv', row.names = FALSE, sep = ',')
}

dataname <- online
                            