---
layout: post
title: Improve Predictive Performance in R with Bagging
date: 2012-01-18 07:49
slug: build-your-own-bagging-function-in-r
modified: 2014-01-07 20:18
status: published
categories: R
---

Bagging, aka bootstrap aggregation, is a relatively simple way to increase the
power of a predictive statistical model by taking multiple random samples(with
replacement) from your training data set, and using each of these samples to
construct a separate model and separate predictions for your test set. These
predictions are then averaged to create a, hopefully more accurate, final
prediction value.  
  
One can quickly intuit that this technique will be more useful when the
predictors are more unstable. In other words, if the random samples that you
draw from your training set are very different, they will generally lead to
very different sets of predictions. This greater variability will lead to a
stronger final result. When the samples are extremely similar, all of the
predictions derived from the samples will likewise be extremely similar,
making bagging a bit superfluous.  
  
Taking smaller samples from your training set will induce greater instability,
but taking samples that are too small will result in useless models.
Generally, some fraction of your training set between 1/50th and 1/2 will be
useful for bagging purposes(of course, this greatly depends on how many
observations are in your training set). The smaller your bagging samples, the
more samples you will need to collect and the more models you will need to
generate to create more stability in the final predictors.  
  
While there are some libraries that will take care of bagging for you in R,
writing your own function allows you a greater degree of control and
understanding over the process, and it is a relatively quick exercise.  
  
Okay, enough theoretical framework. Lets jump into the code. Anyone who wants
more theory can consult [this paper](http://citeseerx.ist.psu.edu/viewdoc/down
load?doi=10.1.1.121.7654&rep=rep1&type=pdf) about bagging.  
  
I'm going to construct a relatively trivial example where a dependent
variable, y, can be predicted by some combination of the independent variables
x1, x2, and x3.  
  

    
    
      
    set.seed(10)  
    y<-c(1:1000)  
    x1<-c(1:1000)*runif(1000,min=0,max=2)  
    x2<-c(1:1000)*runif(1000,min=0,max=2)  
    x3<-c(1:1000)*runif(1000,min=0,max=2)  
    

As you can see, y is a sequence of the values from 1 to 1000. x1, x2, and x3
are permutations of y, but with random errors added. runif generates a
specified number of random numbers from 0 to 1, unless a min and max are
specified, in which case the numbers fall between those values. Each of the x
sequences will roughly approximate y, but with random errors thrown in. The
set.seed function is simply to ensure that the subsequent random number
generation proceeds in a predictable fashion, so that your results match mine.  
  
Fitting a linear model to the variables results in an R squared of .7042:

    
    
      
    lm_fit<-lm(y~x1+x2+x3)  
    summary(lm_fit)  
    

Now we will see how well the x values predict y. First, we designate a random
sample of y to be our "test" set. The rest will be the training set.

    
    
      
    set.seed(10)  
    all_data<-data.frame(y,x1,x2,x3)  
    positions <- sample(nrow(all_data),size=floor((nrow(all_data)/4)*3))  
    training<- all_data[positions,]  
    testing<- all_data[-positions,]  
    

The above code places all of our variables into a data frame, then randomly
selects 3/4 of the data to be the training set, and places the rest into the
testing set.  
  
We are now able to generate predictions for the testing set by creating a
linear model on the training set and applying it to the testing set. We are
also able to calculate the prediction error by subtracting the actual values
from the predicted values (the error calculation here is root mean squared
error):

    
    
      
    lm_fit<-lm(y~x1+x2+x3,data=training)  
    predictions<-predict(lm_fit,newdata=testing)  
    error<-sqrt((sum((testing$y-predictions)^2))/nrow(testing))  
    

The calculated error should be 161.15.  
  
The next step is to run a function that implements bagging. In order to do
this, I will be using the foreach package. Although I will not use it in
parallel mode, this code is designed for parallel execution, and I highly
recommend reading [my
post](http://viksalgorithms.blogspot.com/2012/01/parallel-r-loops-for-windows-
and-linux.html) about how to do it if you do not know how.

    
    
      
    library(foreach)  
    length_divisor<-4  
    iterations<-1000  
    predictions<-foreach(m=1:iterations,.combine=cbind) %do% {  
    training_positions <- sample(nrow(training), size=floor((nrow(training)/length_divisor)))  
    train_pos<-1:nrow(training) %in% training_positions  
    lm_fit<-lm(y~x1+x2+x3,data=training[train_pos,])  
    predict(lm_fit,newdata=testing)  
    }  
    predictions<-rowMeans(predictions)  
    error<-sqrt((sum((testing$y-predictions)^2))/nrow(testing))  
    

The above code randomly samples 1/4 of the training set in each iteration, and
generates predictions for the testing set based the sample. It will execute
the number of time specified by iterations. When iterations was set to 10, I
received an error value of 161.10. At 300 iterations, error went to 161.12, at
500 iterations, error went to 161.19, at 1000 iterations, error went to
161.13, and at 5000 iterations, error went to 161.07. Eventually, bagging will
converge, and more iterations will not help any further. However, the
potential for improvement in results exists. You should be extremely cautious
and assess the stability of the results before deploying this approach,
however, as too few iterations or too large a length divisor can cause
extremely unstable results. This example is trivial, but this can lead to
better results in a more "real-world" application.  
  
Finally, we can place this code into a function to wrap it up nicely:

    
    
      
    bagging<-function(training,testing,length_divisor=4,iterations=1000)  
    {  
    predictions<-foreach(m=1:iterations,.combine=cbind) %do% {  
    training_positions <- sample(nrow(training), size=floor((nrow(training)/length_divisor)))  
    train_pos<-1:nrow(training) %in% training_positions  
    lm_fit<-lm(y~x1+x2+x3,data=training[train_pos,])  
    predict(lm_fit,newdata=testing)  
    }  
    rowMeans(predictions)  
    }  
    

As you can see, bagging can be a useful tool when used correctly. Although
this is a trivial example, you can replace the data and even replace the
simple linear model with more powerful models to make this function more
useful.