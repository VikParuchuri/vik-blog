---
layout: post
title: An easy way to get started with automated essay scoring
date: 2014-03-25 08:28
slug: an-easy-way-to-get-started-with-automatic-essay-scoring
modified: 2014-03-25 08:28
status: published
categories: AES Essay scoring python
---

Wow, it's been way too long since I have updated this blog!  I am going to start making more frequent updates, and I have some cool things in the pipeline, so bear with me.

Last year, I wrote [this post](http://vikparuchuri.com/blog/on-the-automated-scoring-of-essays/) on automated essay scoring.  This was essentially distilling my experience with [automated essay scoring](http://en.wikipedia.org/wiki/Automated_essay_scoring) and trying to introduce it to people unfamiliar with it.  I got a lot of great reaction, and based on this post, and some of my other work in the field, I get a lot of emails about the topic.

Most people who email me want to know how to get started with automated essay scoring.  I always struggle with where to point them, because none of the tools that exist right now (including ones written by me!) are extremely easy to use.

A couple of weeks ago, I reached a tipping point, and told myself that I wouldn't give another person a non-answer, and started working on an easy-to-use, and open source, essay scoring server.  You can find it [here](https://github.com/VikParuchuri/scan).

I will go into more detail about how I made it and how the algorithm works later on, but the keys for now are:

Nontechnical:

* Web interface that makes it easy to create problems and enter essays
* Visual feedback on how the model is scoring
* Easy to install and start using

Technical:

* Good unit test coverage for the algorithm (>90%)
* Easy to develop on with vagrant

The primary caveat is that I made this in 1.5 days.  It works, and people have tested it, but some parts are unpolished, and there are likely bugs that I don't know about.

Please feel free to reach out if you want to contribute, or just want to chat about this.  I'm excited to see how people use it!