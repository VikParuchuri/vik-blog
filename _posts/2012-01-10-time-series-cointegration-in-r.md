---
categories: vik
cover: false
date: 2012-01-10 19:00
layout: post
modified: 2014-01-07 20:18
slug: time-series-cointegration-in-r
status: published
subclass: post
tags: Finance R
---

Cointegration can be a valuable tool in determining the mean reverting
properties of 2 time series. A full description of cointegration can be found
on [Wikipedia](http://en.wikipedia.org/wiki/Cointegration). Essentially, it
seeks to find stationary linear combinations of the two vectors.  
  
The below R code, which has been modified from
[here](http://quanttrader.info/public/testForCoint.html), will test two series
for integration and return the p-value indicating the likelihood of
correlation. It runs significantly faster than the original code, however. I
used this for relatively short time series(50 observations), and while it
functioned relatively quickly for small numbers of series, it became
cumbersome to use when attempting to serially cointegrate over 100k pairs of
bid-ask price series when using it with an mapply function. So scaling up may
be an issue.

    
    
      
    library(tseries)  
    cointegration<-function(x,y)  
    {  
    vals<-data.frame(x,y)  
    beta<-coef(lm(vals[,2]~vals[,1]+0,data=vals))[1]  
    (adf.test(vals[,2]-beta*vals[,1], alternative="stationary", k=0))$p.value  
    }  
    

This runs an [augmented Dickey-Fuller
test](http://en.wikipedia.org/wiki/Augmented_Dickey%E2%80%93Fuller_test) and
will return a p-value indicating whether the series are mean-reverting or not.
You can use the typical p-value as a test of significance if you like(ie, a
p-value below .05 indicates a mean-reverting spread), or you can use an
alternate value. This assumes that your two series were observed at the same
time points. The [original
post](http://quanttrader.info/public/testForCoint.html) that this code as
modified from contains a further description of cointegration, along with more
time series data type handling.