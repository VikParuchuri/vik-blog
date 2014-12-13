---
layout: post
title: Simple speech recognition in Python
date: 2014-04-10 08:28
slug: simple-speech-recognition-in-python
modified: 2014-04-10 08:28
status: published
categories: python speech scribe
---

Sometime today, I got the idea to try to do automatic speech recognition.  Speech recognition, even though it is widely used (and is on our phones), still seems kind of sci-fi-ish to me.  The thought of running it on your own computer is still pretty exciting.

I looked for open source libraries, and was pleasantly surprised to find [Sphinx](http://cmusphinx.sourceforge.net/), a CMU project.  It has python bindings, and even lets you train your own language models (awesome!).

Unfortunately, it was hard to find a working example that takes in audio from a microphone, and does speech recognition on it.  I decided to spend a couple of hours on getting all the configuration and steps down.

It's pretty cool -- you start the python script, say some things, and it converts that audio to text.  Check it out [here](https://github.com/VikParuchuri/scribe).