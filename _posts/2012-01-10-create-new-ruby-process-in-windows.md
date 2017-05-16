---
categories: vik
cover: false
date: 2012-01-10 18:20
layout: post
modified: 2014-01-07 18:47
slug: create-new-ruby-process-in-windows
status: published
subclass: post
tags: Ruby windows parallel
---

I recently had a problem whereby I needed one Ruby program to spawn another
Ruby program, but I did not need or want the two programs to interact after
the second program was instantiated. I solved this issue by using the system
function in Ruby and the Windows start command.  

    
    
    system('start ruby.exe C:\script.rb')

This will create a new Ruby window, which will run the specified script, and
close when it is complete.