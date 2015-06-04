
# this script could test and predict, depend on the parameter 'online'
# online = 0

library('nnet')

generateXy <- function(timeVector, XLength, yLength){
  # using for local
  # to-do
  
  
  result <-list(X = X, y = y)
  return(result)
}

generateX <- function(timeVector, XLength, yLength) {
  # using for online
  
  return(X)
}

# read file, purchaseRedeemTotal, no time

# get purchase firstly

if (online == 0) {
  
  # split train and test, split day is 20140801

  # extract X and y

  # set model and train

  # test on train set

  # test on test set
  
  # write predict on test set into file, need to re-evaluate on Python
  # or just write the mean_squared_error and errorVar

} else {
  # train using whole timeVector, extract X from it

  # predict using the latest XLength timeVector

  # write predict into file
}