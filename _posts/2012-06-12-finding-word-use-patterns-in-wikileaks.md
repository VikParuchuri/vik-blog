---
layout: post
title: Finding Word Use Patterns in Wikileaks Cables
date: 2012-06-12 11:10
slug: finding-word-use-patterns-in-wikileaks
modified: 2014-01-07 21:53
status: published
categories:
    - text mining
    - cables
    - word cloud
    - ggplot
    - wordcloud
    - unclassified
    - government
    - foreign service
    - wikileaks
    - classified
    - R
    - diplomatic
    - nlp
    - natural language processing
    - diplomatic cables
---

6/18: A follow-up to this post is now available
[here](http://viksalgorithms.blogspot.com/2012/06/tracking-us-sentiments-over-
time-in.html).  
  
**Recent Discoveries**  
  
When I was a diplomat, I was always interested in the Wikileaks cables and
what could be done with them. Unfortunately, I never got a chance to look at
the site in depth, due to security policies. Now that the ex- is firmly
prepended to diplomat in my resume, I think that I am finally ready to take
that step.  
I recently realized that the wikileaks cables are available in a handy .sql
file online. This of course allowed me to download all 250,000 and import them
into a database table (I used psql and the /i command).  
If you are interested in obtaining the cables for yourself, you will need to
download the torrent from
[here](http://file.wikileaks.org/torrent/cable_db_full.7z.torrent).  
Let me just clarify here that I will not be printing the text of any of these
cables (which has been done in several newspapers), and that I will not be
using any data that is not readily publicly available online.  
  
**That's great, but what can we do with them?**  
  
After I had the cables, I brainstormed to see what I could actually do with
them that would be interesting. I came up with a few ideas:  

  1. Find how topics have changed over time. 
    * It's reasonable to assume that the focus of the cables would have shifted from “Soviet Union” this and “USSR” that to the Middle East.
  2. Find out what words typify State Department writers. 
    * Anyone who has read cables knows that while they are (mostly) in English, its a strange kind of English.
  3. Find out what words/topics typify secret/classified vs unclassified cables. 
    * What topics are more likely to be classified? Does word choice change in classified vs unclassified cables?
I will get into these topics and more as we continue on through this post.  
  
**Starting to work with the data**  
  
The first thing we need to do is read the data from a database. I interfaced
with my PostgreSQL database via ODBC.  
  

    
    
    channel <- odbcConnect(db_name, uid = "", pwd = "")
    
    
     

Now, let's get all the cables from 2010 onwards:  
  

    
    
    cable_frame <- sqlQuery(channel, "SELECT * from cable WHERE date > '2010-01-01'",   
     stringsAsFactors = FALSE, errors = TRUE)
    
    
     

We can make a plot of which senders sent the most cables from 2010 onwards:  
  

    
    
    last_10 <- tail(sort(table(cable_frame$origin)), 10)  
    qplot(names(last_10), last_10, geom = "bar") + opts(axis.title.x = theme_blank()) +   
     opts(axis.title.y = theme_blank()) + opts(axis.text.x = theme_text(size = 8))
    
      
    ![](https://vik-affirm-assets.s3-us-west-1.amazonaws.com/finding-word-use-patterns-in-wikileaks/chart.png)
    
      
     

  
We can see that the Secretary of State and Embassy Baghdad are the two biggest
offenders.  
  
Now, we can get all of the cables in the database and see how cable traffic
changed over time (or perhaps Wikileaks had a biased sample):  
  

    
    
    all_cables <- sqlQuery(channel, "SELECT * from cable", stringsAsFactors = FALSE,   
     errors = TRUE)
    
    
     date_tab <- table(as.POSIXlt(all_cables$date)$year + 1900)  
    qplot(names(date_tab), as.numeric(date_tab), geom = "bar") + opts(axis.title.x = theme_blank()) +   
     opts(axis.title.y = theme_blank()) + opts(axis.text.x = theme_text(size = 8)) 
    
      
    ![](https://vik-affirm-assets.s3-us-west-1.amazonaws.com/finding-word-use-patterns-in-wikileaks/chart1.png)
    
      
     

  
The amount of cables rises almost exponentially from 2000 until 2009. I'm
assuming that only some of the cables for 2010 were leaked, explaining the low
count there.  
  
We can get rid of the all_cables file, as we won't need it going forward:  

    
    
    rm(all_cables)  
    gc()
    
    
     

**Comparing word usage in the 80's and 90's to word usage today**  
  
Now, we can get to something interesting: we can compare how word usage/topics
shifted from 1980-1995 to today. Because there are relatively few cables from
early on, we have to specify a 15 year range, which nets us only around 675
cables.  
  

    
    
    cable_present <- sqlQuery(channel, "SELECT * from cable WHERE date > '2010-02-15'",   
     stringsAsFactors = FALSE, errors = TRUE)
    
    
     cable_past <- sqlQuery(channel, "SELECT * from cable WHERE date > '1980-01-01' AND date < '1995-01-01'",   
     stringsAsFactors = FALSE, errors = TRUE)
    
    
     

Now, we have two challenges. The cables all have line breaks and returns (\r
and \n), and a lot of the older cables are in all caps. We will get rid of
these issues by removing the breaks/returns and converting everything to all
lower case.  
  

    
    
    ppatterns <- c("\\n", "\\r")  
    combined <- tolower(gsub(paste("(", paste(ppatterns, collapse = "|"),   
     ")", sep = ""), "", c(cable_past$content, cable_present$content)))
    
    
     

Now, we can construct a term document matrix which counts the number of times
each term occurs in each document:  
  

    
    
    corpus <- Corpus(VectorSource(combined))  
    corpus <- tm_map(corpus, stripWhitespace)  
    cable_mat <- as.matrix(TermDocumentMatrix(corpus, control = list(weighting = weightTf,   
     removePunctuation = TRUE, removeNumbers = TRUE, wordLengths = c(4, 15))))  
    cable_mat <- cable_mat[rowSums(cable_mat) > 3, ]
    
    
     

We remove any words that are under 4 characters or over 15 characters, and
additionally remove any terms that appear less than 3 times in the whole group
of cables.  
  
For convenience, we can split the matrix into one containing past cables and
one containing current cables:  
  

    
    
    present_mat <- cable_mat[, (nrow(cable_past) + 1):ncol(cable_mat)]  
    past_mat <- cable_mat[, 1:nrow(cable_past)]  
    rm(cable_mat)  
    gc()
    
    
     

Now we can get to the good stuff and find differential word usage between the
two sets of cables:  
  

    
    
    chisq_vals <- chisq(rowSums(past_mat), ncol(past_mat) * 100, rowSums(present_mat),   
     ncol(present_mat) * 100)  
    chisq_direction <- rep(-1, length(chisq_vals))  
    mean_frame <- data.frame(past_mean = rowSums(past_mat)/ncol(past_mat),   
     present_mean = rowSums(present_mat)/ncol(present_mat))  
    chisq_direction[mean_frame[, 2] > mean_frame[, 1]] <- 1  
    chisq_vals <- chisq_vals * chisq_direction  
    cloud_frame <- data.frame(word = rownames(present_mat), chisq = chisq_vals,   
     past_sum = rowSums(past_mat), present_sum = rowSums(present_mat))  
    pal <- brewer.pal(9, "Set1")
    
    
     

The above code will calculate the statistical difference (chisq) between the
terms in the first set of cables (1980-1995), and the second set (cables from
february 2010).  
  
Now we can make some word clouds. This first cloud contains words that appear
in the 2010 cables in a more significant way than in the 1980-1995 cables. A
larger size indicates that it more significantly appears in the 2010 cables:  
  

    
    
    wordcloud(cloud_frame$word, cloud_frame$chisq, scale = c(8, 0.3),   
     min.freq = 2, max.words = 100, random.order = T, rot.per = 0.15, colors = pal,   
     vfont = c("sans serif", "plain"))  
    

![](https://vik-affirm-assets.s3-us-west-1.amazonaws.com/finding-word-use-
patterns-in-wikileaks/chart2.png)

  
  
This second cloud indicates the words that appear in a significant way in the
1980-1995 cables, but not in the 2010 cables:  
  

    
    
    wordcloud(cloud_frame$word, -cloud_frame$chisq, scale = c(8, 0.3),   
     min.freq = 2, max.words = 100, random.order = T, rot.per = 0.15, colors = pal,   
     vfont = c("sans serif", "plain"))
    
      
    ![](https://vik-affirm-assets.s3-us-west-1.amazonaws.com/finding-word-use-patterns-in-wikileaks/chart3.png)
    
      
     

  
As we can see, february is very significant in the first plot, which is to be
expected, because all of the cables are from february. But, we can also see
interesting patterns, like trafficking becoming very important in 2010 vs
1980-1995, and words like development and training gaining prominence. In the
second plot, we see more interest in topics like zagreb, soviet, saudi, and
croatia.  
  
**Find out what words typify secret/classified cables vs unclassified in 2010**  
  
Let's take a look at what words/topics are more prevalent in secret or
classified cables. Let's first look at how many cables of each type are in our
cable_present data frame:  
  

    
    
    table(cable_present$classification)  
    
    
    
    ##   
    ## CONFIDENTIAL CONFIDENTIAL//NOFORN   
    ## 719 67   
    ## SECRET SECRET//NOFORN   
    ## 188 51   
    ## UNCLASSIFIED UNCLASSIFIED//FOR OFFICIAL USE ONLY   
    ## 643 756   
    

  
Now, we will do something similar to what we did above, where the data was
split into 2 chunks and the words in each chunk were compared to generate
clouds. I have made the code generic by changing the names to set one and set
two.  
  

    
    
    cable_set_one <- cable_present[cable_present$classification %in%   
     c("SECRET", "SECRET//NOFORN"), ]  
    cable_set_two <- cable_present[cable_present$classification %in%   
     c("UNCLASSIFIED", "UNCLASSIFIED//FOR OFFICIAL USE ONLY"), ]  
    ppatterns <- c("\\n", "\\r")  
    combined <- tolower(gsub(paste("(", paste(ppatterns, collapse = "|"),   
     ")", sep = ""), "", c(cable_set_one$content, cable_set_two$content)))  
    corpus <- Corpus(VectorSource(combined))  
    corpus <- tm_map(corpus, stripWhitespace)  
    cable_mat <- as.matrix(TermDocumentMatrix(corpus, control = list(weighting = weightTf,   
     removePunctuation = TRUE, removeNumbers = TRUE, wordLengths = c(4, 15))))  
    cable_mat <- cable_mat[rowSums(cable_mat) > 3, ]  
    one_mat <- cable_mat[, 1:nrow(cable_set_one)]  
    two_mat <- cable_mat[, (nrow(cable_set_one) + 1):ncol(cable_mat)]  
    rm(cable_mat)  
    gc()  
    chisq_vals <- chisq(rowSums(one_mat), ncol(one_mat) * 100, rowSums(two_mat),   
     ncol(two_mat) * 100)  
    chisq_direction <- rep(-1, length(chisq_vals))  
    mean_frame <- data.frame(one_mean = rowSums(one_mat)/ncol(one_mat),   
     two_mean = rowSums(two_mat)/ncol(two_mat))  
    chisq_direction[mean_frame[, 2] > mean_frame[, 1]] <- 1  
    chisq_vals <- chisq_vals * chisq_direction  
    cloud_frame <- data.frame(word = rownames(one_mat), chisq = chisq_vals,   
     one_sum = rowSums(one_mat), two_sum = rowSums(two_mat))  
    pal <- brewer.pal(9, "Set1")
    
    
     

We are now ready to plot these new word clouds. Here are words that are
typical of set 1 (secret cables) that separate it from set 2 (unclassified
cables):  
  

    
    
    wordcloud(cloud_frame$word, -cloud_frame$chisq, scale = c(8, 0.3),   
     min.freq = 2, max.words = 100, random.order = T, rot.per = 0.15, colors = pal,   
     vfont = c("sans serif", "plain"))  
    

![](https://vik-affirm-assets.s3-us-west-1.amazonaws.com/finding-word-use-
patterns-in-wikileaks/chart4.png)

  
  
And here are words that are typical of set 2 (unclassified cables) that
separate it from set 1 (secret cables) :  
  

    
    
    wordcloud(cloud_frame$word, cloud_frame$chisq, scale = c(8, 0.3),   
     min.freq = 2, max.words = 100, random.order = T, rot.per = 0.15, colors = pal,   
     vfont = c("sans serif", "plain"))  
    

![](https://vik-affirm-assets.s3-us-west-1.amazonaws.com/finding-word-use-
patterns-in-wikileaks/chart5.png)

  
  
This makes sense, as the first cloud has words like icbms and bombers, whereas
the second has words like labor and victims, which would be typical of the
trafficking in persons/human rights reports.  
  
**Find out what words typify secret/classified cables vs unclassified from 1960-2000**  
  
Now, we can look at what words differentiated secret cables from unclassified
cables from 1960 to 2000.  
  
Here is the cloud that shows what words appear significantly in the secret
cables, but not in the unclassified cables:  
  

    
    
    wordcloud(cloud_frame$word, -cloud_frame$chisq, scale = c(8, 0.3),   
     min.freq = 2, max.words = 100, random.order = T, rot.per = 0.15, colors = pal,   
     vfont = c("sans serif", "plain"))  
    

![](https://vik-affirm-assets.s3-us-west-1.amazonaws.com/finding-word-use-
patterns-in-wikileaks/chart6.png)

  
  
And here is the cloud that shows what words appear significantly in the
unclassified cables, but not in the secret cables:  
  

    
    
    wordcloud(cloud_frame$word, cloud_frame$chisq, scale = c(8, 0.3),   
     min.freq = 2, max.words = 100, random.order = T, rot.per = 0.15, colors = pal,   
     vfont = c("sans serif", "plain"))  
    

![](https://vik-affirm-assets.s3-us-west-1.amazonaws.com/chart7.png)

  
  
**Conclusion**  
  
It's very interesting to see how these patterns change over time.
Particularly, seeing what the classified topics were from 1960-2000 versus
unclassified is interesting. I really wanted to see how State Department
writers differ from normal english writers, but I don't have the time to do it
right now. It will have to wait for the next post.