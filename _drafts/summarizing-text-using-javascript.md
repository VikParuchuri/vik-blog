---
layout: post
title: Summarizing text using javascript
date: 2014-12-13 08:28
categories: Javascript, summarization
---

Lately, I have been getting more and more into web development.  Which naturally leads to using Javascript.  A lot of Javascript.  I was fully prepared to hate it (I remember trying Javascript close to when I began programming, and it was painful), but it has been a surprisingly fun (or at least okay) experience.  At some point in my Javascript journey, I realized that [chrome extensions](https://chrome.google.com/webstore/category/extensions) are just bundles of javascript, html, and css.  And then I got excited, because chrome extensions can do some very powerful things.  One of the cool things that chrome extensions can do is modify web pages in place.  One of the big problems I have is that too many articles on the internet are interesting, and I end up spending too much time reading them.  Perhaps we can use the cool thing to solve the problem?

The basic idea for a solution is to highlight the most important text in a long article automatically.  Skimming an article is probably not the best idea in every scenario, but there are definitely cases where it is useful.  The nice thing about highlighting in place is that is preserves context.  Want to see what happened before the highlighted sentence?  Want to read the whole article?  Go nuts.  Instead of throwing up barriers to this, like pulling a summary out of the article, highlighting in place lets you gain a deeper understanding if you want to.

Okay, so we have a basic outline of what we want.  How do we actually do this?  The first insight is that most text on the web is surrounded by `<p>` tags.  So we just need to extract the text from those tags, find the important stuff, and put the highlighted text back in.  Easy, right?

The next step is to decide on how we will construct the summaries.  One approach is to crowdsource the summaries.  Unfortunately, I am impatient, and I want summaries now, not after some helpful person decides to do it for me.  We could still use a semi-manual method where I highlight important passages, and the system learns what I consider important over time.  This would actually be really cool, but I am also lazy, and don't want to do all that highlighting.  So purely automated solutions it is.

A long time ago (in internet terms, at least), I used the [textrank](http://acl.ldc.upenn.edu/acl2004/emnlp/pdf/Mihalcea.pdf) algorithm in a python [project](https://gist.github.com/VikParuchuri/6998391).  The basic idea of the textrank algorithm is to find the parts of a piece of text that have the most connections to other parts of the text.  Great, so we could definitely use this algorithm to find the most "connected" sentences, which are probably the most important.

Once we know which sentences are the most important, it should let us highlight them in place by wrapping them with `<span>` tags and applying css styles.

Here is the outline of our plan:

* Pull text out of the webpage.
* Do some sort of preprocessing on the text to make it cleaner.
* Split the text into sentences.
* Split sentences into words.
* Find how similar each sentence is to each other sentence.
    * We can do this by finding how much vocabulary they have in common.
* Construct a graph of sentences, with edges weighted by similarity.
* Use an algorithm (hey, maybe [pagerank](http://en.wikipedia.org/wiki/PageRank)!) to find the most "connected", and therefore important, sentences.
* Highlight the important sentences in place.

So let's get this show on the road!

## Extracting and preprocessing the text

Okay, lets get the text out of the page and split it into smaller units of text.  We can easily grab each paragraph by doing `$('p')` with jquery.  We then have some options in terms of how we want to split the text into sentences and words.  We can use a very simple and naive method, which just splits sentences on periods(`sentences = text.split(". ")`), and words on spaces(`words=sentence.split(' ')`).  There is nothing extremely wrong with this method, but there are definitely better ways to do it.  Thankfully, there is an npm package called [text-parse](https://www.npmjs.org/package/text-parse) that does both types of splits for us.  The advantage of a library here is that it is already presumably well-tested, and we don't have to write the code ourselves.  It also is able to do part of speech tagging, which will help us out later.

One stumbling block is that we want to make a chrome extension, but text-parse is a package for node.  Thankfully, the awesome [browserify](http://browserify.org/) package lets us convert npm packages to javascript files that we can include in html (just like normal js files).  We can use text-parse by doing this:

```shell
npm install text-parse
browserify -r text-parse > bundle.js
```

Then we can just include bundle.js in our chrome extension and do `var parse = require('text-parse')` when we want to use text-parse.

Now, we can move on to the more exciting stuff, namely figuring out how sentences are similar to each other.

## Sentences to hash tables

Now that we can pull text out of each paragraph and process it, we can just loop through all the paragraphs in the document and apply our algorithm.

We basically want to find how similar sentences are by how much vocabulary is shared between them.  We first will split our paragraph into sentences using text-parse, and then into words.  Once we have the set of words in a sentence, we can loop over the words, lowercase them, and store occurrence frequencies in a hash table, with one table per sentence.

Two additional wrinkles before we get started:

* The textrank algorithm paper states that only using adjectives and nouns to find similarities between sentences greatly enhances summarization accuracy.  So, we use our part of speech tagger (through text-parse) and filter to only keep words with parts of speech in the list `["JJ", "JJR", "JJS", "NN", "NNP", "NNPS", "NNS"]`.

* We will eventually be constructing a [sentence-term matrix](http://en.wikipedia.org/wiki/Document-term_matrix) from our hash tables, and applying a [tf-idf](http://en.wikipedia.org/wiki/Tf%E2%80%93idf) transformation to it.  I will explain more about this later, but for now, we will need to keep track of the maximum frequency with which any word occurs in the sentence.

The paragraph "The grass is never greener on the other side.  I am happiest where I am."  would turn into:

```
[
{
   'grass': 1,
   'greener': 1,
   'other': 1,
   'side': 1
},
{
   'i': 2,
   'happiest': 1
}
]
```

And the maximum frequencies would be `1` and `2`.

## Constructing a matrix

We now want to construct a matrix.  In this matrix, each row will be a word, and each column will be a sentence.  Each cell will represent how often that word occurs in that sentence.  We want to do this so that we can efficiently apply different transformations to discover which sentences are "key" to the paragraph.

We now take all the unique tokens across the whole paragraph to construct row names for our matrix.  In this case, `['grass', 'greener', 'other', 'side', 'i', 'happiest'].

