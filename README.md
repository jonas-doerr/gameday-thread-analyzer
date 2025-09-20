# Packers Gameday Thread Analyzer
I'm building a tool to scrape the comments off a Reddit gameday thread, in which fans discuss an ongoing sports game. It will be particularly focused towards analyzing threads in the Green Bay Packers (American football team) subreddit.

## To-do list
- build tool to scrape comments [DONE]
- tokenize comments [DONE]
    - remove some basic stopwords that spacy didn't catch [DONE]
- group and analyze comments

## Concepts Learned
- first, I went to https://praw.readthedocs.io/en/stable/tutorials/comments.html to learn how to get the comments from the Reddit API
- reviewed regex and how to efficiently preprocess words
- learned some basics of the spacy library

## Analysis ideas
- most mentioned names [DONE]
- positive or negative overall sentiment 
- most mentioned words [DONE]
- common themes throughout the thread
- guess whether or not the Packers won

## Journal
### 9.19
I figured out that I can't just leak my Reddit app's secret, so it took my a long time to clear out my old commits and make a new environment that didn't reveal it to everybody. After that, I cleared out some bad words that came up and also some words that didn't get caught by my previous stopwords function inherent to spacy.

### 9.20
I ranked the keywords most commonly seen in the gameday thread. I kept adding new words to my stopwords list, because words like "look" or "good" are not as useful as words like "refs" or "Parsons" (a player name). I also added a list of the Packers roster and used it to look through the lemmatized words and see which players were mentioned the most often. There was some margin of error (for example, parson not counting for Micah Parsons), which I might fix in my next edit.