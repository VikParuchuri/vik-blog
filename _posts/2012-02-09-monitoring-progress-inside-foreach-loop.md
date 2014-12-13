---
layout: post
title: Monitoring Progress Inside a Foreach Loop
date: 2012-02-09 09:12
slug: monitoring-progress-inside-foreach-loop
modified: 2014-01-07 20:31
status: published
categories: foreach randomForest doSnow R
---

The foreach package for R is excellent, and allows for code to easily be run
in parallel. One problem with foreach is that it creates new RScript instances
for each iteration of the loop, which prevents status messages from being
logged to the console output. This is particularly frustrating during long-
running tasks, when we are often unsure how much longer we need to wait, or
even if the code is doing what it is intended to. The solution to this can be
found in the sink() function. This function redirects output to a file. I will
show you a simple example of this using the iris data set. The code below will
execute without printing any status messages, even though do.trace is enabled,
which periodically displays the status of the randomForest. The random forest
code is slightly adapted from one of the foreach package examples.

    
    
      
    library(foreach)  
    library(doSNOW)  
    library(randomForest)  
    data(iris)  
      
    cores<-2  
      
    num_trees<-ceiling(2000/cores)  
    c1<-makeCluster(cores)  
    registerDoSNOW(c1)  
      
    rf_fit<-foreach(ntree=rep(num_trees,cores),.combine=combine,  
    .packages=c("randomForest")) %dopar% {  
    randomForest(iris[,-5],y=iris[,5],ntree=ntree,do.trace=100)   
    }  
      
    stopCluster(c1)   
      
    

We can easily correct this with the sink function:

    
    
      
    library(foreach)  
    library(doSNOW)  
    library(randomForest)  
    data(iris)  
      
    cores<-2  
      
    num_trees<-ceiling(2000/cores)  
    c1<-makeCluster(cores)  
    registerDoSNOW(c1)  
      
    writeLines(c(""), "log.txt")  
      
    rf_fit<-foreach(ntree=rep(num_trees,cores),.combine=combine,  
    .packages=c("randomForest")) %dopar% {  
    sink("log.txt", append=TRUE)  
    randomForest(iris[,-5],y=iris[,5],ntree=ntree,do.trace=100)   
    }  
      
    stopCluster(c1)  
    

The writeLines function will clear out the file "log.txt" before the loop is
run, ensuring that only output that is relevant to the current run is
displayed when the file is opened. The log file can be opened at any time
during the run, and the progress can be checked. We can even print the number
of the iteration as we go through:

    
    
      
    rf_fit<-foreach(iteration=1:cores,ntree=rep(num_trees,cores),  
    .combine=combine,.packages=c("randomForest")) %dopar% {  
    sink("log.txt", append=TRUE)  
    cat(paste("Starting iteration",iteration,"\n"))  
    randomForest(iris[,-5],y=iris[,5],ntree=ntree,do.trace=100)   
    }  
    

This is useful when you have significantly more iterations than processor
cores, and you want to know how far along you are.