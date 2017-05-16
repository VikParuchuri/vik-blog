---
categories: vik
cover: false
date: 2012-01-23 18:47
layout: post
modified: 2014-01-07 20:26
slug: analyzing-us-government-contract-awards
status: published
subclass: post
tags: data-analysis government spending R
title: Analyzing US Government Contract Awards in R
---

As I was exploring open data sources, I came across [USA
spending](http://usaspending.gov/). This site contains information on US
government contract awards and other disbursements, such as grants and loans.
In this post, we will look at data on contracts awarded in the state of
Maryland in the fiscal year 2011, which is available by selecting "Maryland"
as the state where the contract was received and awarded
[here](http://usaspending.gov/data?carryfilters=on). I will use Maryland as a
proxy for the nation, as the data set for the whole nation will be a bit more
unwieldy to analyze, and the USA spending site appears to need a significant
amount of time to generate the data file for it. We may take a look at the
data for the whole nation later on.  
  
First, we download the data file(leave all the options on the usa spending
site the same, except select Maryland as the state where the contracts were
received and performed when you download the file if you want to follow
along), and read it into R:  

    
    
    spend<-read.csv(file="marylandspendingbasic.csv",  
    head=TRUE,sep=",",stringsAsFactors=FALSE,strip.white=TRUE)  
    

By using the names() function, we can see that the data file has a lot of
interesting columns. One column is called extentcompeted, and has values
indicating how much competition was involved in the bidding process for the
contracts. Understandably, having an open bidding process is in the public
interest as it can reduce taxpayer costs. We will start by looking at
competition in the bidding process for contracts:  

    
    
    library(ggplot2)  
    competition<-tapply(spend$ExtentCompeted,spend$ExtentCompeted,  
    function(x) length(x)/length(spend$ExtentCompeted))  
      
    qplot(names(competition),weight=competition*100,xlab="Competition Type",  
    ylab="Percent of Contracts",fill=names(competition))   
    + opts(axis.text.x = theme_blank())   
    + scale_fill_discrete("Competition Type")  
    

This lets us see what percentage of the data falls into each competition
category, and then graphs it using the excellent ggplot2 package.  

![](https://vik-affirm-assets.s3-us-west-1.amazonaws.com/competition.png)

This shows us that about 58% of contracts went through a full competitive
bidding process, whereas only approximately 15% of the contracts did not
undergo any kind of competition process.  
  
Now, lets see how many dollars of spending fall into each competition
category:  

    
    
    comp_dollars<-tapply(spend$DollarsObligated,spend$ExtentCompeted,  
    function(x) sum(x)/sum(spend$DollarsObligated,na.rm=TRUE))  
    qplot(names(comp_dollars),weight=comp_dollars*100,xlab="Competition Type",  
    ylab="Percentage of Dollars Obligated",fill=names(comp_dollars))   
    + opts(axis.text.x = theme_blank())   
    + scale_fill_discrete("Competition Type")  
    

![](https://vik-affirm-assets.s3-us-west-1.amazonaws.com/comp_dollars.png)

This plot tells a very different story, showing that about 31% of all dollars
that were spent by the government went to contracts that did not involve
competition. Further, only 44.5% of all dollars that were obligated went to
contracts that were bid on under a fair and open competitive bidding process.  
  
This indicates that large contracts tend to receive less bidding than small
contracts. This is strange, as large contracts are the ones that are more
likely to have reduced costs as a result of competitive bidding, simply
because saving 5% of a larger sum is preferable to saving 5% of a smaller sum.
Let's take a look at where these large no-bid contracts are going.  
  

    
    
    companies<-sort(tapply(spend$DollarsObligated,spend$RecipientName,sum))  
    top_companies<-tail(companies/sum(spend$DollarsObligated),10)*100  
    sum(spend$DollarsObligated/1e9)  
    qplot(names(top_companies),weight=top_companies,xlab="Company",  
    ylab="Percentage of Total Dollars Obligated",fill=names(top_companies))   
    + opts(axis.text.x = theme_blank())   
    + scale_fill_discrete("Company Name")   
    + opts(legend.text = theme_text(size = 8))  
    

![](https://vik-affirm-assets.s3-us-west-1.amazonaws.com/companies.png)

First, we note that 15.7 billion dollars in federal contracts were obligated
to vendors in the state of Maryland in the fiscal year 2011. Next, we note
that about 11.5% of the total federal money allocated in contracts went to
Lockheed Martin! In fact, the top 10 companies in terms of dollar value of
contracts received were given 41% of all the contracted dollars, which amounts
to about 6.5 billion dollars. The top 100 contractors received 72% of all
contracted dollars. Now, it is becoming clearer where the large no-bid
contracts are going. We will look more in depth at the contracts that did not
involve competitive bidding to zero in on the issue:

    
    
      
    nc_spend<-spend[spend$ExtentCompeted=="Not Competed under SAP"   
    | spend$ExtentCompeted=="Not Competed"   
    | spend$ExtentCompeted=="Not Available for Competition"   
    | spend$ExtentCompeted=="Full and Open Competition after exclusion of sources",]  
    nc_companies<-sort(tapply(nc_spend$DollarsObligated,nc_spend$RecipientName,sum))  
    nc_top_companies<-tail(nc_companies/sum(nc_spend$DollarsObligated),10)*100  
    sum(nc_spend$DollarsObligated)/1e9  
    sum(tail(nc_companies,10))/sum(nc_spend$DollarsObligated)  
    

This tells us that out of the 7.6 billion dollars in government contracts that
were disbursed with limited or no competition, 55% of these went to the top 10
contractors who received contracts with limited or no competition. This shows
that large contractors tend to receive a much greater share of no compete
contracts than other contractors, as the top 10 contractors only received 41%
of all federal dollars, yet received 55% of contracts with limited
competition.

    
    
      
    mean(nc_spend$DollarsObligated)  
    mean(spend[spend$ExtentCompeted=="Full and Open Competition",]$DollarsObligated)  
    

This shows that the average contract size with no or limited competition was
$253507.1, whereas the average contract size with full and open competition
was $113936.3, meaning that, on average, contracts twice as large are given
out with no competition.  
  
I will leave this analysis here for now, but please feel free to continue on
if you wish. This is a very interesting data set, and I may come back to it if
I have time down the line.