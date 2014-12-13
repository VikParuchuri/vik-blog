---
layout: post
title: Using LaTeX, R, and Sweave to Create Reports in Windows
date: 2012-01-30 18:24
slug: using-latex-r-and-sweave-to-create
modified: 2014-01-07 20:31
status: published
categories: Windows LaTeX Sweave R
---

[LaTeX](http://www.latex-project.org/) is a typesetting system that can easily
be used to create reports and scientific articles, and has excellent
formatting options for displaying code and mathematical formulas.
[Sweave](http://www.statistik.lmu.de/%7Eleisch/Sweave/) is a package in base R
that can execute R code embedded in LaTeX files and display the output. This
can be used to generate reports and quickly fix errors when needed.  
  
There are some barriers to entry with LaTeX that seem much steeper than they
actually are. In this article, I will show you how to setup LaTeX and an IDE
for it in Windows, and how to start developing for it. Note that you will at
least R version 2.14 to follow this entire article, because the command line
sweave pdf export option was added then.  
  
**Install MiKTeX and TeXnicCenter**  
  
LaTeX documents are edited in a text editor, then compiled by a compiler, and
finally are displayed in a PDF or postscript viewer. We will begin by
installing a LaTeX compiler for Windows, [MiKTeX](http://miktex.org/). Once
you grab the installer, you can go ahead and install it. Please see the bottom
of the post for the full edit, but installing LaTeX in paths with spaces in
them can cause issues. As such, I would recommend installing to a directory
without them.  
  
Our next step will be to install [TeXnicCenter](http://www.texniccenter.org/),
an IDE for LaTeX. After installing TeXnicCenter and starting it for the first
time, you will be asked to find your LaTeX executable file in the
configuration wizard. This can generally be found in the folder C:\Program
Files\MiKTeX 2.9\miktex\bin by default, or a custom path if you did not use
spaces in your path. You can leave the fields for PostScript viewer blank,
unless you need the functionality. You should now be finished with the
installation.  
  
**Setup TeXnicCenter to Work with Sweave**  
  
Now, we can setup TeXnicCenter to use Sweave directly. This will require at
least R 2.14. To do this, click on the Build menu and go to Define Output
Profiles. Hit the "Add" button in the bottom left to create a new output
profile. You can name the profile anything you like. I named mine "Sweave".  
  
Now we need to configure the new output profile. The first tab should look
similar to mine if you use 64-bit R, but your R path will be different if you
use 32-bit or used a non-default installation directory. The directory will
need to match yours. The command line arguments box should read: CMD Sweave
--pdf %nm .  

![](https://vik-affirm-assets.s3-us-west-1.amazonaws.com/sweave2.png)

Now, we only need to worry about the viewer tab. I use Foxit Reader, so my
settings are below. I suggest using the same settings as you find in your
LaTeX=>PDF output profile.  

![](https://vik-affirm-assets.s3-us-west-1.amazonaws.com/sweave3.png)

Once we have all that set, you can go ahead and write your first document. You
will need to name the document something.Rnw. To build the file, you will have
to select "Sweave"(or whatever you named your profile" in the drop down box
below the build item on the menu bar, and then select Build->Current
File->Build and View to build your first file.  

![](https://vik-affirm-assets.s3-us-west-1.amazonaws.com/sweave4.png)

The above shows a trivial R script. <<>>= signifies the start of an R script,
and @ signifies the end.  
  
**Further Reading**  
  
To learn more about Sweave, I suggest reading the [user
manual](http://www.stat.uni-muenchen.de/%7Eleisch/Sweave/Sweave-manual.pdf).
[Here](http://stackoverflow.com/questions/8366193/writing-big-documents-with-
sweave-is-it-possible-to-do-as-with-latex) is a good discussion of workflow
with big documents and Sweave. To learn more about LaTeX, I suggest the [LaTeX
wikibook](http://en.wikibooks.org/wiki/LaTeX), and [The Not So Short
Introduction to LaTeX](http://tobi.oetiker.ch/lshort/lshort.pdf). [This
page](http://amath.colorado.edu/documentation/LaTeX/basics/example.html) shows
how to make a basic document in LaTeX, and can be a good template to work off
of. This [link](http://sachaem47.fortyseven.versio.nl/latexcourse/lec4/SweaveI
nstall.pdf) gave me some of the concepts used above, and also has instructions
for how to use Stangle with TeXnicCenter.  
  
**Edit** A commenter has pointed out that using a directory path with spaces in it can create bugs in LaTeX. You can find more information on this [here](http://tex.stackexchange.com/questions/4315/include-image-with-spaces-in-path-directory-to-be-processed-with-dvips), and [here](http://groups.google.com/group/latexusersgroup/browse_thread/thread/f78aab8bdaedcdf7?pli=1). I have updated my post.