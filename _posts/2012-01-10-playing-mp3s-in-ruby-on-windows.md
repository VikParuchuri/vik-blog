---
categories: vik
cover: false
date: 2012-01-10 18:38
layout: post
modified: 2014-01-07 18:46
slug: playing-mp3s-in-ruby-on-windows
status: published
subclass: post
tags: Ruby Windows
---

I recently needed to play music in Ruby in order to create an alarm clock of
sorts. The code to do this was (surprise surprise) fairly simple, but I want
to post it for posterity.

    
    
      
    require 'win32ole'  
    player = WIN32OLE.new('WMPlayer.OCX')  
    player.OpenPlayer('C:\alarm.mp3')  
    

This will open a new instance of Windows Media Player that plays the selected
song.  
  
Note that win32ole should be installed by default, and does not need to be
installed as a gem.