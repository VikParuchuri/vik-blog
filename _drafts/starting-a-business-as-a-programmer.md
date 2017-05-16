---
layout: post
cover: false
title: Starting a business as a programmer
date: 2017-05-13 05:00
categories: vik
tags: business life
subclass: post
---

I haven't written a blog post here in quite a while.  For the past 2 years, I've been building [Dataquest](https://www.dataquest.io), a site that's helped thousands of people become data scientists or data analysts.  Although I started Dataquest as a solo technical founder, this post isn't about that adventure -- it's about the time between leaving my previous job, at [edX](https://www.edx.org), an online education company, and starting to work on Dataquest.

I left edX at the beginning of 2014, and I started Dataquest in early 2015.  In the almost 2 years in between, I worked on everything from small side projects to incorporated companies with co-founders.  Along the way, I learned a lot about what types of businesses to work on (and which types not to work on).  As is all too common, most of these lessons are only apparent in retrospect.

When I left edX, I had only been a professional programmer for about a year, so my network was extremely limited.  I didn't have a great understanding of how tech companies actually worked at any level.  By sharing some of the lessons I've learned over the years, I'm hoping to help people like me -- people who are technically skilled, and dream of making an impact on the world, but don't know what to start or how to start it.  In this post, I'll share insights on each of the projects I worked on, why they didn't become *the* project, and the lessons I learned.

## Percept

The first project I worked on was while I was still at edX.  It was called [percept](https://github.com/VikParuchuri/percept), and it was a modular framework for machine learning.  The goal was to enable people to:

* Write their own "modules" that would preprocess data, perform machine learning, and do analysis
* Chain these modules together to perform repeatable analysis on data
* Use modules contributed by others to avoid having to re-write commonly used modules (like certain data cleaning steps)

The idea for percept came out of my own pain points when doing data science work.  I'd have to manually re-write a lot of boilerplate whenever I approached a new dataset, and I guessed that others had a similar problem.  I actually developed percept to the point where I was able to use it to do well on a [Kaggle competition](https://www.kaggle.com/c/cause-effect-pairs).

