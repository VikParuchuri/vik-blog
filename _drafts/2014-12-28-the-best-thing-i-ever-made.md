---
layout: post
title: The best thing I ever coded, or the story of how I stayed sane at a boring job
date: 2014-12-28 08:28
slug: the-best-thing-i-ever-coded
modified: 2014-12-28 08:28
status: published
categories: Java coding
---

In January of 2011, I joined the US Foreign Service.  Along with 80 others, I went through a class called A-100, and got a crash course on how to be a diplomat.  We learned how to address foreign dignitaries.  We got lessons in diplomatic history.  There was even an optional class on how to comport yourself at diplomatic dinners (I skipped this one).  At the end of training, we were ready to change the face of US foreign relations.

In June, I was sent to Georgetown, Guyana, for a two year assignment (a "tour" at a "post" in Foreign Service lingo).  During the first year of my tour, I was to do consular work, and then switch to economic work for the second.  Consular work includes three major areas: nonimmigrant visas, immigrant visas, and american citizen services.  The main commonality between all of them is paperwork.  Lots of it.

### The passport process
  
  All new consular officers at my post were assigned to do pre-processing of immigrant visas.  These visas were for people who wanted to migrate to the US and get permanent resident status, so we needed to do a lot of checks to ensure that their applications were legitimate.  The task that fell to me was to go through the passport of each person who was applying for an immigrant visa.  I then had to get the passport number and their name.  I then had to do a few things:
  
  * Search a database (let's call it "DB1") for previous visa applications
    * Search by passport number, and see if any hits came up.
    * Search a database for their name, and see if any hits came up.
    * Guyana is a country where assumed names are common, and some people don't have a last name, so search for variations of the name on the passport.
    * For each hit that was returned, click on the record, wait for it to open, and print it out.
  * Search a different database ("DB2") for criminal and other history
    * Use the passport number, name, and assumed names to search.
    * For any hits that came up, print each record out.
  * All of the printouts were then put in the applicants' file so the officer who interviewed them for their visa could have all the information in one place.
    
I quickly came to loathe this process.  Because we were using very old computers, we only had Internet Explorer 6, and each page could take 10-20 seconds to load.  Going through the whole process took two hours (I usually had 20-30 of these to do per day), and it was two hours of unending monotony and boredom.  Open a passport, read a name, type in a name, click once to search, click 1-10 times on each record that comes up, and print each one out.  Repeat several times for each database.  I still sometimes look back on the whole process and get unreasonably angry -- it was a convoluted mess that absolutely should have been automated, and I feel incredibly sorry for anyone who has had to do it.

### Using Excel

I went through the whole process for about a week before I realized that I needed to fix it to retain my sanity.  I starting optimizing parts of the process.  The first thing I did was go through all of the passports at the same time, and type everything into Excel.  I could then do all of the checks without going back and forth between the computer and the passports.  I deleted the file at the end of the process, for security (none of the information was classified or secure, but we had guidelines for handling sensitive information).  Net savings from this step was about 10 minutes.  I felt kind of good about taking a first step, but I wasn't satisfied -- the work was still pretty horrible.

### Automating a single search

I had taken a Java class in highschool, and I knew the basics of how to program.  A crazy idea came to me -- one any experienced programmer would have probably shot down immediately or found a better way to accomplish.  I decided to write a program that clicked on things.  The basic idea was that I was entering a name, then clicking on a few things in a predictable sequence.  What if a program could move the mouse and click for me?  I would save a ton of time.  The major wrinkle was handling the varying number of records in the DB1 -- sometimes there were none, sometimes 1, sometimes 10, and so on.

I stayed up at night reading about Java, and started doing some simple coding at home and at work.  The nice thing about Java was that I didn't need to install anything -- Java was already on the computer, and I could just download and run eclipse USB edition without installing it.  I decided to make a simple program that displayed one button in the window -- the button was marked "Run".  You had to navigate to the starting search screen of DB1 and enter a name or passport number into the search form.  Then you hit "Run", and some cool stuff happened:

* It moved the cursor over the "search" button in the form, and clicked it to run the search.
* It waited 30 seconds for the search to finish.
* The results were presented in a list, and each result was a link (and therefore was blue).  The results started at certain screen coordinates (let's say (600,500)), and then each result would be 20px below the previous one.  So, I first tested the color at (600,500).  If it was blue, I clicked the link.  Then:
    * Wait 30 seconds for the result page to load.
    * Click "File" then "print" (I forget the exact menu structure in IE6)
    * Hit "next" once on the print dialog and then click "print"
    * At this point, the print dialog went away, and the page was printed out.
    * Click the "back" button to go back to the results page.
    * Add 20px to the y axis of the screen coordinate to test.
    * Test the color.  If blue, then click on the link and go back to the top of these instructions.  If not blue, end the program.

This was way better than what I had before!  I could type in a name, hit the "Run" button in my program dialog, and come back to a screen full of purple links, and a printer full of printouts.  It prevented me from having to click on each report, and improved my sanity a lot.  But I still had to enter each name manually, and go back and forth a lot to enter the next name.  Sometimes, IE would throw an error or some other condition, and it would cause the program to fail (it would go on clicking in its own sequence, but the clicks wouldn't do what it was expecting).  It also didn't help at all with DB2, which still had to be searched manually.

Net savings from this step was about 30 minutes.

### Automating many searches

I realized that the bottleneck was me -- if I didn't have to go back and forth and type in each name manually, I could save a ton of time.  I wondered if there was a way to get data from Excel into Java, so that Java could type in the names for me and run the searches.  I read up on ODBC, and how to read excel worksheets from Java.  I also read up on how to simulate keyboard entry with Java, and how to show file picker dialogs.

The "Run" button morphed, so that now when you clicked it, it popped up a file chooser.  You picked a worksheet (in .xls format, I didn't know how much easier csv is!), and then it was loaded in.  The first column of the worksheet was the person's name, and the second column was the passport number.  

The program went through each row of the worksheet and:
    
* Clicked on the "first name" box, and typed in the person's first name.
* Clicked on the "last name" box, and typed in the person's last name.
* Ran a search, and then followed the steps to automate a single search above.
* Clicked "back" when that was done, to go back to the search form.
* Erased the data in the "first name" and "last name" boxes.
* Clicked on the "passport number" field and entered it.
* Re-ran the search, and repeated the steps from automating a single search.

By the end, I had a nice stack of printouts!  All I had to do was enter all of the passport information into the sheet in the right format.  This was a major leap forward, and made my life much much better.  I still had to do all of the DB2 searches manually though, and that was a pain.

Net savings here were about 40 minutes.  I had automated the process down from 2 hours to 40 minutes -- a savings of 6 hours and 40 minutes a week.  Things were looking up, but there was still more work to do!

### A hacky way to use alt-tab


