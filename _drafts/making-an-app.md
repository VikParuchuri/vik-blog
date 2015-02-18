---
layout: post
title: Making an app as a (belated) Valentine's day gift
date: 2015-02-18 18:20
status: published
categories: android app tulalens
---

For the past year, my girlfriend, [Priya](https://twitter.com/priyabiyer) has been working on an awesome nonprofit called [Tulalens](http://www.tulalens.org).  The idea is to be "yelp for low-income people in emerging markets".  She did a pilot in October/November 2014 where she and the Tulalens team went into the slums of [Hyderabad](http://en.wikipedia.org/wiki/Hyderabad), and surveyed pregnant women on which hospitals they went to and the quality of care they received.  She was then able to analyze the data and figure out the best hospitals in the area.  

Knowing this, she went back to the same women, and told them about the available hospitals, cost, and their quality.  The information asymmetry is startling -- some women were taking buses and travelling 20+ kilometers for appointments when better hospitals were much closer.  Another woman was paying bribes to get basic care in a government hospital.  All told, 25% of women changed hospitals after hearing about the new alternatives, 43% talked to their providers about getting better care, and 100% talked with their families about the information.

{:.center}
![Surveying](/images/tulalens/surveying.jpg)  
Here's Syed (a data collector on the Tulalens team) surveying a young woman

She wants to scale up her process, and is going back to India in a week to do a larger survey.  The only problem?  She and her team were using android tablets to collect data.  Essentially, you go to a house, talk to a woman, and record her responses into an app while having a conversation.  As there is no internet access in the slums, this needs to work offline.  The available apps to do this kind of work are very limited, and most are pretty bad.  She was using an app that cost ~100 dollars a month for a few users, but rapidly climbed in price to a few thousand dollars a month.  It also didn't have all of the features she wanted (multiple language support, ability to edit responses after they were given, ability to identify who collected which response, ability to skip some questions, etc).

Priya's worked hard to find people who can help her make an app, and two awesome people even helped make a [prototype](http://challengepost.com/software/tulolens) at a hackathon last weekend.  It's really hard as a non-technical person to network and find people who can help, but Priya's also found people who can help with making analysis scripts, and do other work.  The challenge is pulling all the threads together and building a production-ready survey system that can be used in a week.

I love the work that Tulalens is doing, and I owe Priya for putting up with me all these years, so I decided to help her make the app as a Valentine's day gift.  I'm terrible at getting gifts (I remember getting a dress a couple of sizes too big once, but as a plus, I did get some awesome earrings), and Priya doesn't ever ask for anything, so this seemed like a good fit.  The only challenge?  I'm working on [Dataquest](https://www.dataquest.io), so I only had about a day to work on the app (this day was Monday (2/16), if anyone is keeping score).

## Getting started (8am - 9am)

I spent a little bit of time looking for existing apps that were good for offline surveying.  I found a lot of projects that appeared dead, but couldn't find anything good.  Lacking time, I moved on to building.

It had been a couple of years since I touched Java and Android development, and I remembered it being painful.  I was right, but not immediately.  The installation actually went pretty well.  I first installed [Android Studio](http://developer.android.com/sdk/index.html), then had to grab the [JDK](http://www.oracle.com/technetwork/java/javase/downloads/jdk7-downloads-1880260.html).

I then imported the existing prototype app and took a look at it.  

{:.center}
![Prototype](/images/tulalens/prototype.png)  
Login screen from the prototype

I spent some time playing around with the prototype.  It was very well done for having been done in an overnight hackathon that was ~16 hours (7:30pm - 12pm the next day).  I'm not sure why this particular format was picked, but it may have had something to do with most of the participants being college students, and having scheduling conflicts.

The good with the prototype:

* It implemented an authoring platform in-app for surveys.
* It had individual user accounts.
* It used parse, which is always a great first choice for an app backend.
* It was an app people made because they cared about Tulalens (this is awesome!)

The problems with the prototype:

* It crashed after some questions were answered.
* It didn't have a way to update/edit questions.
* Survey answering wasn't fully implemented.

Ultimately, rather than spend time trying to re-architect the app, I took some design decisions from it and started fresh with a new app.  This was because the time to re-architect the app was unknown, but I knew I could make an app from scratch in a day.  I can't emphasize enough how awesome it was that Leo and Jeffrey took the time to work on this.

## The fun part! (10am - 10:30am)

Making surveys on-device is a very helpful feature, but it wasn't strictly necessary, so I decided to skip it and make survey authoring happen on a computer.  The surveys could then be synced over to [Parse](http://www.parse.com), which is just a database in the cloud, and accessed from the app.

I googled a bit looking for a good standard survey format, but couldn't find one.  I would have searched some more, but time constraints meant that I needed to make one.

I made a yaml format for surveys that looks like this:

~~~~~~~~
----------

name: Test Survey
description: Figure out stuff about people
survey_number: 1
language: english
author: Test Guy

----------

type: choice_single
question: |
  What kind of person are you?
options:
  - Choice 1
  - Choice 2
  - Choice 3
  - Choice 4
next_screen:
  - 2
  - 2
  - 3
  - 3
  
-----------

type: text
question: |
  Where are you going next?
  
----------
~~~~~~~~

Sections are delimited by 4 or more dashes (-----). The top section is metadata about the survey, and each subsequent section is a screen in the survey.  `next_screen` refers to the number of the screen that will be shown, depending on the response.  With some questions, like `Do you own a phone`, you want to be able to skip some subsequent questions if someone answers `No`.

The other types of questions were `choice_multiple` (choose multiple options), `text` (freeform text response), and `integer` (integer response).

I whipped up a quick database schema for the surveys and screens, and a python  command to sync all the surveys that were put in a folder.  [Parsepy](https://github.com/dgrtwo/ParsePy) was a huge help with the syncing.  

Surveys are uniquely identified by `survey_number`.  The database schema stores a version number, so you can update a survey, and all the versions will be stored.  Each screen is stored as a row, with a foreign key to the screen.  This way, each version of the survey has its own screens, so you never get confusion over whether someone answered the old version of a question, or the new version.

This was the fun part because I'm already really comfortable with python, and that's why doing all of this was so quick.  The final code for this step is online [here](https://github.com/VikParuchuri/tulalens-survey-web).

## First steps with making an app (10am-11am)

I started fresh with a new app in Android studio.  It's on Github [here](https://github.com/VikParuchuri/TulaLensSurvey).  I used the navigation drawer template because it seemed easier than writing my own navigation.  After Android Studio created an app skeleton, I stared around for a while trying to re-familiarize myself with Java and the structure of Android programs.  I'm not ashamed to say that there was some frenzied googling and looking at stackoverflow.

I needed to first integrate the Parse SDK into the app.  I wasted an embarrassingly large amount of time wondering why I was getting errors about `symbol parse not found`, when I had just forgotten to import it in the main activity of the app, but eventually got over this hump.

After Parse was integrated, I could add in a login screen with just a couple of lines of code.
   

{:.center}
![Login](/images/tulalens/login.png)  
The login screen.  Yes, it's super light, and should be fixed.

## Adding a listview and sync (11am - 1pm)

I now needed a way to list out surveys on the device, and to sync them.  I decided to use a `ListView` to do this, with the `ParseQueryAdapter`.  This is a parse builtin class that will do a query to the parse database, and present the results in a list.  I used the parse concept of [pinning](http://blog.parse.com/2014/04/30/take-your-app-offline-with-parse-local-datastore/) to only show surveys in the local database to the listview (the listview doesn't access the internet).

Basically, the data flow is Parse Cloud -> Local Datastore -> Listview.

I needed to build a sync service to get data from the cloud to the local datastore.  I used a query, along with pinning, to store all the current surveys (latest versions) to the local datastore.  The list view could then pick these up and show them.

{:.center}
![Survey List](/images/tulalens/surveys.png)  
The survey list screen.  The sync button is at the top right.

## Adding a settings view with login/logout (1pm - 1:30pm)

I now needed to add a way for people to log out if they wanted.  Priya has three tablets, and different people will be using each at different times, so they all need to be able to sign in under their own account.  The logout isn't fully implemented (you need to force-close the app after you log out to get back to the login screen), but it works for now.

{:.center}
![Settings](/images/tulalens/logout.png)  
The settings view with the logout button.

## The hard part!  The survey engine (1:30pm - 3pm)

I now had to work on the hardest part, rendering the surveys dynamically from the database schema.  I made a new fragment called `EngineFragment` to be the survey rendering engine.  When you click on a survey in the surveys list, this fragment is initialized.  It loads the database schema, figures out what type of question needs to be shown, and loads and shows a layout accordingly.

Different types of questions have different fields that are shown.

{:.center}
![Survey MC](/images/tulalens/survey_mc.png)  
A survey with the choice_single type.  You can pick one option.  The next button goes to the next screen.  The bar at the bottom was added later, and will be explained later.

{:.center}
![Survey Text](/images/tulalens/survey_text.png)  
A survey with the text type.  You can enter any text you want.

The hardest part here was dynamically rendering any amount of fields for the `choice_single` and `choice_multiple` types.  I solved this by creating the views dynamically and adding them to the layout.

## Storing the responses (3pm - 4pm)

Once someone hits "Next", the response to the question should be stored.  In order to do this, I pulled out the right value depending on what the question type was, and created a new `ScreenAttempt` model.  This model was associated with a screen (which is associated with a survey object that has a version), so you can keep track of who answered what.  A participant id is also generated every time a new survey is started, so you can see which responses were given by which woman.

I used the parse `saveEventually` function to store these responses whenever a network connection was found.

## Setting up everything on windows (4pm - 5:30pm)

This was honestly the most frustrating part, and involved setting up Python on Priya's computer so she could run the scripts and update the surveys while she's in India.  She's a Windows user, sadly.  We got python setup, thanks to [Anaconda](https://store.continuum.io/cshop/anaconda/), but Android Studio just didn't want to work when it came time to import the app project.

While I worked on helping her, Priya was setting up her tablets and installing all the needed software (Pycharm, Java, Android Studio, Anaconda, Git, etc).

## Pushing the app to Google Play (5:30pm - 5:45pm)

Because we couldn't get Android Studio setup on her computer, we needed a way to distribute app updates to the tablets.  I pushed the app to Google Play alpha testing (needed to add some screenshot, and generate a keystore) so it could be downloaded remotely.

## User Testing and Bug Fixes (ongoing)

Priya started testing out a lot of the functionality once everything was setup, and started finding some bugs, and needed features.  Some of the things we've addressed:

* Ability to remove surveys from the survey list.
* Ability to go back and edit responses a woman gave if the conversation reveals new information. (this is the seek bar in the screenshots above)
* Crash when using certain values in survey options

{:.center}
![Priya Vik](/images/tulalens/priya-vik.jpg)  
Here we are super spaced out after climbing Mt. Cadillac in Maine.  I don't have a good picture from after coding this app up, but this approximates our mental states.

## Conclusions

I'm really excited to see this app used, and it's really rewarding to have had the chance to help out with this.  If you want to contribute drop Priya a line -- she's priya at tulalens.org, and TulaLens is on twitter [@tulalens](https://twitter.com/tulalens).  The app is on Github [here](https://github.com/VikParuchuri/TulaLensSurvey), and the survey authoring part is [here](https://github.com/VikParuchuri/tulalens-survey-web) if you want to take a look.