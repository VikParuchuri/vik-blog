---
layout: post
title: Introduction to Kaggle Algorithmic Trading Challenge
date: 2012-01-10 18:35
slug: introduction-to-kaggle-algorithmic
modified: 2014-01-07 18:47
status: published
categories: Finance Kaggle Algorithms R
---

I recently participated in the Kaggle Algorithmic Trading Competition under
the username VikP. For those who do not know what [Kaggle](http://kaggle.com)
is, it is a web site where individuals and corporations can host data analysis
competitions. This particular
[competition](http://www.kaggle.com/c/AlgorithmicTradingChallenge) involved
the prediction of how the prices of 50,000 observations of 102 different
securities at the tick level recovered after both buyer and seller initiated
liquidity shocks.  
  
Each competitor was provided with approximately 750,000 rows of training data,
each of which corresponded to a separate liquidity shock event. Each row
contained observations of the bid and ask prices and an event indicator(trade
event or quote event) for the 50 time points immediately preceding the
liquidity shock, and the bid and ask prices alone for the 50 events
immediately following the event. There was also metadata provided, such as the
number of shares that were traded to create the liquidity shock event and
whether the event was buyer or seller initiated.  
  
There were some limitations to what predictions could be made from the data,
notably because volume information was missing for each trade. Because the
evaluation metric was RMSE, which valued higher prices stocks much more highly
lower priced ones, the competition became heavily dependent on filtering
outliers.  
  
I had a great time participating, enjoyed the high level of competition, and
highly recommend Kaggle competitions to aspiring data miners. During the
competition, I gained many insights into tick data and into analysis of
financial data. I will share some of these insights in the next week or so,
but I just wanted to introduce the competition first!