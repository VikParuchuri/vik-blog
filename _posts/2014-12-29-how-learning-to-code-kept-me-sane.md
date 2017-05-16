---
categories: vik
cover: false
date: 2014-12-29 12:50
layout: post
modified: 2014-12-29 12:50
slug: how-learning-to-code-kept-me-sane
status: published
subclass: post
tags: Java coding
title: How learning to code kept me sane when I was a diplomat
---

In January of 2011, I joined the [US Foreign Service](http://en.wikipedia.org/wiki/United_States_Foreign_Service).  Along with 80 others, I went through a class called [A-100](http://en.wikipedia.org/wiki/A-100_Class), and got a crash course on how to be a diplomat.  We learned how to address foreign dignitaries.  We got lessons in diplomatic history.  There was even an optional class on how to comport yourself at diplomatic dinners (I skipped this one).  At the end of training, we were ready to change the face of US foreign relations.

In June, I was sent to [Georgetown, Guyana](http://en.wikipedia.org/wiki/Georgetown,_Guyana), for a two year assignment (a "tour" at a "post" in Foreign Service lingo).  During the first year of my tour, I was to do [consular work](http://careers.state.gov/work/foreign-service/officer/career-tracks), and then switch to economic work for the second.  Consular work covers three major areas: nonimmigrant visas (people who want to visit the US), immigrant visas (people who want to become permanent residents of the US), and american citizen services (visiting american citizens in jail, etc).  The main commonality between all of them is paperwork.  Lots of it.

{:.center}
![Georgetown,Guyana](/images/best-thing/georgetown.jpg)  
The famous Stabroek market in Georgetown

### Pre-processing immigrant visas
  
  All new consular officers at my post were assigned to do pre-processing of immigrant visas.  These visas were for people who wanted to migrate to the US and get permanent resident status, so we needed to do a lot of checks to ensure that their applications were legitimate.  The task that fell to me was to go through the passport of each person who was applying for an immigrant visa.  I had to get the passport number and their name.  I then had to do a few things (I am obfuscating this process a bit because the State Department teaches you to be very paranoid):
  
  * Search an online database (let's call it "DB1") for previous visa applications
    * Search by passport number, and see if any hits came up.
    * Search a database for their name, and see if any hits came up.
    * Guyana is a country where assumed names are common, and some people don't have a last name, so search for variations of the name on the passport.
    * For each hit that was returned, click on the record, wait for it to open, and print it out.
  * Search a different database with a separate program ("DB2") for criminal and other history
    * Use the passport number and name to search.
    * Only one record would come up, so print it out.
  * All of the printouts were then put in the applicants' file so the officer who interviewed them for their visa could have all the information in one place.
    
I quickly came to loathe this process.  Because we were using very old computers, we only had Internet Explorer 6, and each page could take 10-20 seconds to load.  Going through the whole process took two hours (I usually had 20-30 of these to do per day), and it was two hours of unending monotony and boredom.  Open a passport, read a name, type in a name, click once to search, click 1-10 times on each record that comes up (DB1 could have multiple records for a single name), and print each one out.  And that was just for DB1.  I still sometimes look back on the whole process and get unreasonably angry -- it was a convoluted mess that absolutely should have been automated, and I feel incredibly sorry for anyone who has had to do it.

{:.center}
![IE6](/images/best-thing/ie6.gif)  
Remember IE6?  I wish I didn't

### Using Excel

I went through the whole process for about a week before I realized that I needed to fix it to retain my sanity.  I starting optimizing parts of the process.  The first thing I did was go through all of the passports at the same time, and type everything into Excel.  I could then do all of the checks without going back and forth between the computer and the passports.  I deleted the file at the end of the process, for security (none of the information was classified or secure, but we had guidelines for handling sensitive information).  Net savings from this step was about 10 minutes.  I felt kind of good about taking a first step, but I wasn't satisfied -- the work was still pretty horrible.

{:.center}
![Excel](/images/best-thing/excel.gif)  
If you never used Excel, its a spreadsheet tool

### Automating a single search

I had taken a [Java](http://en.wikipedia.org/wiki/Java_%28programming_language%29) class in high school, and I knew the very basics of how to program.  A crazy idea came to me -- one any experienced programmer would have probably shot down immediately or found a better way to accomplish.  I decided to write a program that clicked on things.  The basic idea was that I was entering a name, then clicking on a few things in a predictable sequence.  What if a program could move the mouse and click for me?  I would save a ton of time.  The major wrinkle was handling the varying number of records in the DB1 -- sometimes there were none, sometimes 1, sometimes 10, and so on.

I stayed up at night reading about Java, and started doing some simple coding at home.  I read some programming books online, the names of which escape me now.  I installed [Eclipse](http://en.wikipedia.org/wiki/Eclipse_%28software%29) at home, and started writing programs.  I remember my joy when I first made a program move the cursor -- it's very cool to step back from a computer and see a program you made clicking on things.

The nice thing about Java was that I didn't need to install anything at work -- Java was already on the computer, and I could just download and run [eclipse portable](http://sourceforge.net/projects/eclipseportable/) edition without installing it.  I decided to make a simple program that displayed one button in the window -- the button was marked "Run".  You had to navigate to the starting search screen of DB1 and enter a name or passport number into the search form.  Then you brought up the program and hit "Run", and some cool stuff happened:

* It moved the cursor over the "search" button in the form, and clicked it to run the search.
* It waited 30 seconds for the search to finish.
* The results were presented in a list, and each result was a link (and therefore was blue).  The results started at certain screen coordinates (let's say (600,500) -- screen coordinates are in pixels, so if you have a 1920x1080 pixel resolution monitor, (600,500) is close to the center, but in the top left corner), and then each result would be 20 pixels below the previous one.  So, I first tested the color at (600,500) on the screen.  If it was blue, I clicked the link.  Then:
    * Wait 30 seconds for the result page to load.
    * Click "File" then "print" (I forget the exact menu structure in IE6)
    * Hit "next" once on the print dialog and then click "print"
    * At this point, the print dialog went away, and the page was printed out.
    * Click the "back" button to go back to the results page.
    * Add 20 to the y axis of the screen coordinate to test.
    * Test the color.  If blue, then click on the link and go back to the top of these instructions.  If not blue, end the program.

This was way better than what I had before!  I could type in a name, hit the "Run" button in my program dialog, and come back to a screen full of purple links, and a printer full of printouts.  It prevented me from having to click on each report, and improved my sanity a lot.  But I still had to enter each name manually, and go back and forth a lot to enter the next name.  I also couldn't really use my computer while the program was running, so I started reading books at my desk.  

It didn't help at all with DB2, which still had to be searched manually.  I then had to put all of the printouts from DB1 together with the matching record from DB2 and put them into the applicant's file.

Net savings from this step was about 30 minutes a day.

### Automating many searches

I realized that the bottleneck was me -- if I didn't have to type in each name manually and click "Run", I could save a ton of time.  I wondered if there was a way to get data from Excel into Java, so that Java could type in the names for me and run the searches.  I read up on [ODBC](http://en.wikipedia.org/wiki/Open_Database_Connectivity), and how to read excel worksheets from Java.  I also read up on how to simulate keyboard entry with Java, and how to show file picker dialogs.

The "Run" button morphed, so that now when you clicked it, it popped up a file chooser.  You picked a worksheet (in .xls format, I didn't know how much easier csv is!), and then it was loaded in.  The first column of the worksheet was the person's name, the second column was the passport number, and each row was a different person.

{:.center}
![Chooser](/images/best-thing/java-chooser.gif)  
A Java file chooser

The program went through each row of the worksheet and:

* Went to the DB1 search page
* Clicked on the "first name" box, and typed in the person's first name.
* Clicked on the "last name" box, and typed in the person's last name.
* Ran a search, and then followed the steps to automate a single search above.
* Clicked "back" when that was done, to go back to the search form.
* Erased the data in the "first name" and "last name" boxes.
* Clicked on the "passport number" field and entered it.
* Re-ran the search, and repeated the steps from automating a single search.

By the end, I had a nice stack of printouts!  All I had to do was enter all of the passport information into the spreadsheet in the right format.  This was a major leap forward, and made my life much much better.  I still had to do all of the DB2 searches manually though, and go through the stack of DB1 printouts to match the records from DB1 and DB2, and that was a pain.

Net savings here were about 40 minutes.  I had automated the process down from 2 hours to 40 minutes a day -- a savings of 6 hours and 40 minutes a week.  Things were looking up, but there was still more work to do!

### A hacky way to use alt-tab

If you use Windows a lot, you know about the alt+tab key combination -- it lets you switch between programs.  You hold them both together, then release the tab key while holding the alt key.  This will show a mini window with the active programs in a set order.  Then, every time you press tab, it highlights the next program in the window.  Whenever you release alt, it will switch to the highlighted program.  Using alt-tab helped me switch to DB2 and print out the DB1 and DB2 records together, so I didn't need to collate them manually.

{:.center}
![Alt-tab](/images/best-thing/alt-tab.png)  
The alt-tab mini-window
  
The process looked something like this:
    
* Print out hits from DB1 for a given name/passport number combo
* Alt-tab to DB2
* Run a search on DB2 and print out records
* Alt-tab back to DB1 and go to the next person

The alt-tab code worked using keypress events.  It then used pixel color recognition to figure out which programs were open.  I made this simpler by only leaving Internet Explorer, Java, and DB2 open (DB2 was a separate program).

The alt-tab code worked like this:

* Set tabCounter to 1.
* Hold alt and tab, then release tab, and hit tab tabCounter number of times.
* Test the pixel at some top left coordinate in the current program (I found a coordinate that was a different color in the three programs)
* If it is the program you want, stay here.  Otherwise, increment tab counter by one, and try alt-tabbing again.
* If you went through 3 alt-tab cycles without getting the program you want, something is wrong, so stop the program.

DB2 was much easier because you didn't have to search for name and passport number (so you only searched once), and only one record came up, so you only had to print once.  The search process was very similar to DB1 -- enter the information needed, and click "Search", then print the page out and go back to the search form.

With this method, all I really needed to do was enter all the passport information into Excel, and then I could just let it run.  I set it up on an unused computer in the office, and just let it run while I did other work.  I would come back to a nicely collated stack of printouts that I could then put into the proper applicant files.  I would sometimes just stare at the program working -- it's oddly mesmerizing to see the cursor moving and clicking on things automatically.

Net savings was 20 minutes a day.  I was now saving 8 hours and 20 minutes a week with my program!  I was really happy, and much more sane than I was before, although I still had to do nonimmigrant visa interviews (another story, but very draining).

### Conclusion

I didn't know it at the time, but that program was one of the best things I've made, if not the best.  It solved a real problem, and saved me time.  It made my life in Guyana much better (loved my tour, but that's also another story).  Best of all, it sparked my own curiosity and love of programming.  I was always a mediocre student at best, and making that program motivated me in a way that school never could.  It showed me what was possible.
  
Almost exactly 1 year after I made that program, I cut my tour short, sold most of my stuff, and came back to the US.  I learned programming (starting with machine learning, fun!), and never looked back.  I've managed to make a lot of things that have helped people since then, but few of them can equal what I made then.

Life's too short to be filled with tedium.  If you ever have a chance to automate your job, take it.  You'll never know where it might take you.  It might even completely change the path you were on.