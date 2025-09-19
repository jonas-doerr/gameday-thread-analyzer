# Packers Gameday Thread Analyzer
I'm building a tool to scrape the comments off a Reddit gameday thread, in which fans discuss an ongoing sports game. It will be particularly focused towards analyzing threads in the Green Bay Packers (American football team) subreddit.

## To-do list
- build tool to scrape comments [DONE]
- tokenize comments [DONE]
    - remove some basic stopwords that spacy didn't catch
- group and analyze comments

## Concepts Learned
- first, I went to https://praw.readthedocs.io/en/stable/tutorials/comments.html to learn how to get the comments from the Reddit API
- reviewed regex and how to efficiently preprocess words
- learned some basics of the spacy library

## Analysis ideas
- most mentioned names
- positive or negative overall sentiment
- most mentioned words
- common themes throughout the thread

## Journal
### 9.19
I figured out that I can't just leak my Reddit app's secret, so it took my a long time to clear out my old commits and make a new environment that didn't reveal it to everybody. After that, I cleared out some bad words that came up and also some words that didn't get caught by my previous stopwords function inherent to spacy.