import praw
import re
import emoji
import spacy
from dotenv import load_dotenv
import os
from collections import Counter
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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
week_2_thread = "https://www.reddit.com/r/GreenBayPackers/comments/1neojbv/week_2_game_thread_washington_commanders_green/"
week_3_thread = "https://www.reddit.com/r/GreenBayPackers/comments/1nmww8q/week_3_game_thread_green_bay_packers_cleveland/"
week_3_postgame_thread = "https://www.reddit.com/r/GreenBayPackers/comments/1nn25mu/week_3_post_game_thread_green_bay_packers/"
week_2_postgame_thread = "https://www.reddit.com/r/GreenBayPackers/comments/1nesr4u/week_2_post_game_thread_washington_commanders/"
submission = reddit.submission(url=week_3_postgame_thread)
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
stopwords = ['m', 's', 'non', 've', 'not', 'see', 'talk', 'game', 'play', 'like', 'get', 'good', 'bad', 'go', 'need']
bad_words = ['fuck', 'shit', 'ass', 'bitch', 'damn']
lemma_comments = [
    c[0] + '*' * (len(c) - 1) if c in bad_words else c
    for c in lemma_comments
    if c not in stopwords]
lemma_comments = ["parsons" if c == "parson" else c for c in lemma_comments]

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
    ["Jordann", "Morgan"], ["Arron", "Mosby"], ["Luke", "Musgrave"], ["Isaiah", "Neyor"],
    ["Nick", "Niemann"], ["Keisean", "Nixon"], ["Kitan", "Oladapo"], ["Collin", "Oliver"],
    ["Matthew", "Orzech"], ["Micah", "Parsons"], ["Jayden", "Reed"], ["Sean", "Rhyan"],
    ["Micahh", "Robinson"], ["Will", "Sheppard"], ["Jaylin", "Simpson"], ["Ben", "Sims"],
    ["Barryn", "Sorrell"], ["Nazir", "Stackhouse"], ["Pierre", "Strong"], ["Zach", "Tom"],
    ["Clayton", "Tune"], ["Carrington", "Valentine"], ["Lukas", "Van Ness"], ["Eric", "Wilson"],
    ["Christian", "Watson"], ["Tory", "Whittington"], ["Dontayvion", "Wicks"], ["Devonte", "Wyatt"]]
packers_lowercase_roster = [[player.lower() for player in full_name] for full_name in packers_roster]
mentioned_player = Counter()
for c in lemma_comments:
    for first, last in packers_lowercase_roster:
        if c == first or c == last:
            full_name = f"{first.title()} {last.title()}"
            mentioned_player[full_name] += 1

top_players = [player for player, _ in mentioned_player.most_common(5)]
print(mentioned_player.most_common(5))
# print(top_players)

# analyze overall sentiment of comments
# nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()
sentiment_scores = [sia.polarity_scores(c) for c in cleaned_comments]

positive_comments = 0
negative_comments = 0
neutral_comments = 0
#lump scores into positive or negative
for score in sentiment_scores:
    if score['compound'] > 0.05:
        positive_comments += 1
    elif score['compound'] > -0.05:
        neutral_comments += 1
    else:
        negative_comments += 1
print(f"Postive comments: {positive_comments}\nNegative comments: {negative_comments}")
if positive_comments > negative_comments:
    print("It seems like the Packers won this game.")
else:
    print("It seems like the Packers lost this game.")

# analyze sentiment towards most mentioned players
player_comments = {player: [] for player in top_players}
for comment in cleaned_comments:
    for player in top_players:
        first, last = player.split()
        if first.lower() in comment or last.lower() in comment:
            player_comments[player].append(comment)
player_sentiments = {player: [sia.polarity_scores(c) for c in player_comments[player]] for player in top_players}
# compile sentiments into an average overall score per player
average_player_sentiments = {}
for player, scores in player_sentiments.items():
    if scores:
        compounds = [s["compound"] for s in scores]
        average_player_sentiments[player] = sum(compounds) / len(compounds)
    else:
        average_player_sentiments[player] = 0.0
print(average_player_sentiments)