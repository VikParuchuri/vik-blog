---
layout: post
title: Loading and/or Installing Packages Programmatically
date: 2012-05-08 05:03
slug: loading-andor-installing-packages
modified: 2014-01-07 20:31
status: published
categories: packages deployment production install load R
---

In R, the traditional way to load packages can sometimes lead to situations
where several lines of code need to be written just to load packages. These
lines can cause errors if the packages are not installed, and can also be hard
to maintain, particularly during deployment.  
  
Fortunately, there is a way to create a function in R that will automatically
load our packages for us. In this post, I will walk you through conceiving and
creating such a function.  
  
In order to write a function that checks if a package is installed, loads it
if it is, and installs it if it isn't, we first need a way to check if a
package is installed. Thankfully, this function does the job:

    
    
      
    is_installed <- function(mypkg) is.element(mypkg, installed.packages()[,1])  
    

The above function comes from a post on the R mailing list, although I do not
know if it is the original source. This function will test if a given function
name is in the list of installed packages. We can access the list directly by
using installed.packages()[,1] , and we can use the function by trying
is_installed("foreach") .  
  
Now that we know how to test if a package is installed or not, we can move on
to writing the function. At this moment, we have two hurdles. The first is how
to load a package from a character vector of names. The second is how to
install a package programmatically. Typically, loading a package will look
like this:

    
    
      
    library(MASS)  
    

Fortunately for us, there is a character.only option in the library function
that allows us to specify the package name as a string.

    
    
      
    library("MASS",character.only=TRUE)  
    

The above gives us the functionality that we need to pass the name of a
package to a function as a string and have it loaded. Now, we need to find how
to install packages, which can be done with the install.packages function:

    
    
      
    install.packages("MASS",repos="http://lib.stat.cmu.edu/R/CRAN")  
    

Explicitly setting the repo will avoid having R ask us for it when the
function is executed for the first time. I chose statlib for convenience, but
feel free to use any repo you like.  
  
Now, we have a way to test if a package is installed, a way to install the
package, and a way to load the package. All we need to do is wrap it up with
an if statement.

    
    
      
    if(!is_installed(package_name))  
    {  
     install.packages(package_name,repos="http://lib.stat.cmu.edu/R/CRAN")  
    }  
    library(package_name,character.only=TRUE,quietly=TRUE,verbose=FALSE)  
    

The above if statement will test to see if a package is installed, and then
install it if it isn't. It will then load the package.  
  
This gets us most of the way to what we want, but if we want to pass a
character vector to the function and have it load multiple packages at once,
we need to wrap everything in a for loop.

    
    
      
    for(package_name in package_names)  
    {  
     if(!is_installed(package_name))  
     {  
     install.packages(package_name,repos="http://lib.stat.cmu.edu/R/CRAN")  
     }  
     library(package_name,character.only=TRUE,quietly=TRUE,verbose=FALSE)  
    }  
    

This for loop will perform the operations that we need on the character vector
package_names. Now, we can just wrap everything into a neat function that is
passed a character vector called package_names.

    
    
      
    load_or_install<-function(package_names)  
    {  
     for(package_name in package_names)  
     {  
     if(!is_installed(package_name))  
     {  
     install.packages(package_name,repos="http://lib.stat.cmu.edu/R/CRAN")  
     }  
     library(package_name,character.only=TRUE,quietly=TRUE,verbose=FALSE)  
     }  
    }  
    

We can call the function with the following syntax (substitute the function
names with your own):

    
    
      
    load_or_install(c("foreach","MASS","doParallel"))  
    

And with that, we are done, and now have a function that can load or install
packages as needed from a character vector. This function will terminate with
an error if the install.packages function or the library function cannot find
the specified package name, but you can fix that by using a try statement,
which is an exercise that I will leave to you for the moment.