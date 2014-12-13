---
layout: post
title: Using R in Ruby
date: 2012-01-10 18:08
slug: using-r-in-ruby
modified: 2014-01-07 20:44
status: published
categories: Ruby Windows R
---

Integrating R into more traditional programming languages can be incredibly
rewarding due to R's powerful built-in statistical tools, but it can also be
extremely frustrating at times. Thankfully, like much else to do with Ruby,
integrating R and Ruby is quite a simple process. To begin, install the gem
rinruby and require it in your script.  
  

    
    
    gem install rinruby
    
    
      
    require 'rubygems'  
    require 'rinruby'  
    

There is no further installation or configuration required. To evaluate an R
expression, use the R.eval command.  

    
    
     R.eval "test=1*1"

To get a value from R, use the R.pull command.

    
    
     test=R.pull "test" 

If you are running large code blocks, it is easy to use the R.eval command
with the R source function. This will evaluate the R instructions in a given
text file.

    
    
    R.eval "source('C:/randomscript.R')"

If you are receiving the below error when attempting to load packages, your R
library path is not properly set in your rinruby created instance of R.

    
    
    Error in library(x) : there is no package called 'x'

You can correct this using the R .libPaths() function.

    
    
    R.eval('.libPaths("C:/Users/R library path")')

To find out what your R library paths are, you should use the Sys.getenv
function in R.

    
    
    Sys.getenv(c("R_LIBS", "R_LIBS_USER"))

You should make sure that you set your library paths in the R instance created
by rinruby to the same paths that appear when you run the Sys.getenv command
in your R GUI. A list of other useful environment variables can be found
[here](http://stat.ethz.ch/R-manual/R-patched/library/base/html/EnvVar.html).
Another useful function to use in conjunction with rinruby is the setwd
command.

    
    
    R.eval('setwd("C:/Users/Documents")')

If you replace the file path above with your R working directory path, rinruby
will save files in the right spot.  
  
**Notes:**  
  
When typing file paths into Ruby for use in R, one should always use the
forward slash(/), or four backslashes(\\\\\\\\), as single and double
backslashes will not escape properly.  
  
Note that using the R.pull command with multiple R instructions(or using it
with the source() function) will often cause long runtimes, or will not
complete. Using the R.eval command to evaluate scripts, and then using the
R.pull command to pull variables out after the script has finished executing
will solve this issue.  
  
You can find more information on this at the
[rinruby](https://sites.google.com/a/ddahl.org/rinruby-users/) site.