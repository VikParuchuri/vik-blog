---
layout: post
title: Parallel R Model Prediction Building and Analytics
date: 2012-01-26 19:13
slug: parallel-r-model-prediction-building
modified: 2014-01-07 20:28
status: published
categories: foreach loop parallel R
---

Modifying R code to run in parallel can lead to huge performance gains.
Although a significant amount of code can easily be run in parallel, there are
some learning techniques, such as the Support Vector Machine, that cannot be
easily parallelized. However, there is an often overlooked way to speed up
these and other models. It involves executing the code that generates
predictions and other analytics in parallel, instead of executing the model
building phase in parallel, which is sometimes impossible. I will show you how
this can be done in this post.  
  
First, we will set up our variables. The setup is fairly similar to the one I
have used in other posts, but note that the length of the vectors has been
increased by a magnitude of 100 to more easily show how much time can be saved
by parallelizing the prediction building phase.

    
    
      
    set.seed(10)  
    y<-c(1:100000)  
    x1<-c(1:100000)*runif(100000,min=0,max=2)  
    x2<-c(1:100000)*runif(100000,min=0,max=2)  
    x3<-c(1:100000)*runif(100000,min=0,max=2)  
      
    all_data<-data.frame(y,x1,x2,x3)  
    positions <- sample(nrow(all_data),size=floor((nrow(all_data)/4)*3))  
    training<- all_data[positions,]  
    testing<- all_data[-positions,]  
    

We now have a testing set of 25,000 rows, and a training set of 75,000 rows,
which is somewhat linear. We will train an SVM on this data. Note that it may
take more than 10 minutes to train an SVM on this data, particularly if you
have an older computer. If you do have an older computer, feel free to reduce
the number of rows in the data frame as needed.

    
    
      
    library(e1071)  
    svm_fit<-svm(y~x1+x2+x3,data=training)  
    svm_predictions<-predict(svm_fit,newdata=testing)  
    error<-sqrt((sum((testing$y-svm_predictions)^2))/nrow(testing))  
    error  
    

After we have built the model, we generate predictions for it, which yields an
error of 13045.9 for me(although this may be different for your data). Our
next step is timing the prediction phase to see how long it takes.

    
    
      
    system.time(predict(svm_fit,newdata=testing))  
    

On my system, this took 35.1 seconds.  
  
We are now ready to set up our parallel infrastructure. I run Windows, and
will use foreach and doSNOW here, although you can certainly use other
parallel packages here if you prefer. You can read [this
post](http://vikparuchuri.com/blog/parallel-r-loops-for-windows-and-
linux.html) if you want an introduction to foreach, doSNOW, and doMC. If you
do not elect to use doSNOW, you will not need to use the stopCluster()
function that appears in some of the code below.

    
    
      
    library(foreach)  
    library(doSNOW)  
    cl<-makeCluster(4) #change the 4 to your number of CPU cores  
    registerDoSNOW(cl)   
    

Now, we have the groundwork for our parallel foreach loop, but we need to find
a way to split the data up in order to perform predictions on small sets of
data in parallel.

    
    
      
    num_splits<-4  
    split_testing<-sort(rank(1:nrow(testing))%%4)  
    

This will create a numeric vector that can be used to split the testing data
frame into 4 parts. I suggest setting num_splits to some multiple of your
number of CPU cores in order to execute the below foreach loop as quickly as
possible. Now that we have a way to split the data up, we can go ahead and
create a loop that will generate predictions in parallel.

    
    
      
    svm_predictions<-foreach(i=unique(split_testing),  
    .combine=c,.packages=c("e1071")) %dopar% {  
    as.numeric(predict(svm_fit,newdata=testing[split_testing==i,]))  
    }  
    stopCluster(c1)  
    

It is very important that the .packages argument be used to load the package
that corresponds to the prediction function you are going to use in the loop,
or R will get confused about which prediction function to use and generate an
error. The .combine argument tells the foreach loop to combine the outputs of
the foreach loop into a vector. A hidden argument that defaults to true
ensures that all the outputs remain in order.  
  
Now, we test to make sure that everything is okay by checking what the error
value is:

    
    
      
    error<-sqrt((sum((testing$y-svm_predictions)^2))/nrow(testing))  
    error  
    

I got 13045.9, which matches the value I got before, and confirms that both
the parallel and non-parallel prediction routines return the exact same
results.  
  
Now, we can create a function and time it to see how fast the parallel
technique is:

    
    
      
    parallel_predictions<-function(fit,testing)  
    {  
    cl<-makeCluster(4)  
    registerDoSNOW(cl)  
    num_splits<-4  
    split_testing<-sort(rank(1:nrow(testing))%%4)  
    predictions<-foreach(i=unique(split_testing),  
    .combine=c,.packages=c("e1071")) %dopar% {  
    as.numeric(predict(fit,newdata=testing[split_testing==i,]))  
    }  
    stopCluster(cl)  
    predictions  
    }  
      
    system.time(parallel_predictions(svm_fit,testing))  
    

This takes 12.76 seconds on my system, which is significantly faster than the
non-parallel implementation.  
  
This technique can be extended to other analytics functions that can be run
after the model is built, and it can generate predictions for any model, not
just for the svm that the example uses. While creating the model can take up
much more time than generating predictions, it is not always feasible to
parallelize model creation. Running the prediction phase in parallel,
particularly on high dimensional data, can save significant time.