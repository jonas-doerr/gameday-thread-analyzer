import praw
import re
import emoji
import spacy
from dotenv import load_dotenv
import os

load_dotenv()

def preprocess_comment(comment: str) -> str:
    comment = comment.lower() # lowercase
    comment = re.sub(r"http\S+", "", comment) # remove links
    comment = re.sub(r"[^a-z0-9\s]", "", comment) # remove punctuation
    comment = emoji.replace_emoji(comment, replace = "") # remove emojis
    comment = comment.replace("\n", " ") # there's a bunch a \n for new lines that show up, this removes them
    comment = re.sub(r"\s+", " ", comment).strip() # prevents multiple spaces
    return comment

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="packers_analysis"
)

# fetch comments from reddit thread
thread_link = "https://www.reddit.com/r/GreenBayPackers/comments/1neojbv/week_2_game_thread_washington_commanders_green/"
submission = reddit.submission(url=thread_link)
print("fetching comments") #debug in case gets laggy
submission.comments.replace_more(limit=10) #it takes a while if I take too many comments
print("done fetching") #also for debugging purposes
comments = [comment.body for comment in submission.comments.list()[:20]]

# preprocess text
cleaned_comments = [preprocess_comment(c) for c in comments]

# tokenize text with spacy
nlp = spacy.load("en_core_web_sm")
spacy_doc = [nlp(c) for c in cleaned_comments]
lemma_comments = [
    token.lemma_ 
    for doc in spacy_doc
    for token in doc
    if not token.is_stop and token.is_alpha] # removes numbers and stopwords

# stopwords that didn't get caught
stopwords = ['m', 's', 'non', 've']
bad_words = ['fuck', 'shit', 'ass', 'bitch', 'damn']
lemma_comments = [
    c[0] + '*' * (len(c) - 1) if c in bad_words else c
    for c in lemma_comments
    if c not in stopwords]

print(lemma_comments)