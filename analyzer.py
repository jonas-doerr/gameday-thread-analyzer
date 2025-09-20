import praw
import re
import emoji
import spacy
from dotenv import load_dotenv
import os
from collections import Counter

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
comments = [comment.body for comment in submission.comments.list()]

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
stopwords = ['m', 's', 'non', 've', 'not', 'see', 'talk', 'game', 'play', 'like', 'get', 'good', 'bad']
bad_words = ['fuck', 'shit', 'ass', 'bitch', 'damn']
lemma_comments = [
    c[0] + '*' * (len(c) - 1) if c in bad_words else c
    for c in lemma_comments
    if c not in stopwords]

#find keywords
ranked_keywords = Counter(lemma_comments).most_common(10)
print(ranked_keywords)

#check which players were mentioned the most
packers_roster = [["Israel", "Abanikanda"], ["Deslin", "Alexandre"], ["Zayne", "Anderson"], ["Johnathan", "Baldwin"],
    ["Aaron", "Banks"], ["Brant", "Banks"], ["Anthony", "Belton"], ["Warren", "Brinson"],
    ["Chris", "Brooks"], ["Karl", "Brooks"], ["Javon", "Bullard"], ["Dalton", "Cooper"],
    ["Edgerrin", "Cooper"], ["Brenton", "Cox"], ["Romeo", "Doubs"], ["Kingsley", "Enagbare"],
    ["James", "Ester"], ["John", "FitzPatrick"], ["Rashan", "Gary"], ["Travis", "Glover"],
    ["Matthew", "Golden"], ["Kamal", "Hadden"], ["Mecole", "Hardman"], ["Malik", "Heath"],
    ["Nate", "Hobbs"], ["Ty'Ron", "Hopper"], ["Josh", "Jacobs"], ["Elgton", "Jenkins"],
    ["Donovan", "Jennings"], ["Jamon", "Johnson"], ["Darian", "Kinnard"], ["Tucker", "Kraft"],
    ["MarShawn", "Lloyd"], ["Jordan", "Love"], ["Isaiah", "McDuffie"], ["Xavier", "McKinney"],
    ["Brandon", "McManus"], ["Mark", "McNamee"], ["Bo", "Melton"], ["Jacob", "Monk"],
    ["Jordan", "Morgan"], ["Arron", "Mosby"], ["Luke", "Musgrave"], ["Isaiah", "Neyor"],
    ["Nick", "Niemann"], ["Keisean", "Nixon"], ["Kitan", "Oladapo"], ["Collin", "Oliver"],
    ["Matthew", "Orzech"], ["Micah", "Parsons"], ["Jayden", "Reed"], ["Sean", "Rhyan"],
    ["Micah", "Robinson"], ["Will", "Sheppard"], ["Jaylin", "Simpson"], ["Ben", "Sims"],
    ["Barryn", "Sorrell"], ["Nazir", "Stackhouse"], ["Pierre", "Strong"], ["Zach", "Tom"],
    ["Clayton", "Tune"], ["Carrington", "Valentine"], ["Lukas", "Van Ness"], ["Eric", "Wilson"],
    ["Christian", "Watson"], ["Tory", "Whittington"], ["Dontayvion", "Wicks"], ["Devonte", "Wyatt"]]
packers_lowercase_roster = [[player.lower() for player in full_name] for full_name in packers_roster]
mentioned_player = {}
for c in lemma_comments:
    for first, last in packers_lowercase_roster:
        if c == first or c == last:
            full_name = f"{first.title()} {last.title()}"
            mentioned_player[full_name] = mentioned_player.get(full_name, 0) + 1

print(mentioned_player)
