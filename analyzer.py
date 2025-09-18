import praw
import re
import emoji
import spacy

def preprocess_comment(comment: str) -> str:
    comment = comment.lower() # lowercase
    comment = re.sub(r"http\S+", "", comment) # remove links
    comment = re.sub(r"[^a-z0-9\s]", "", comment) # remove punctuation
    comment = emoji.replace_emoji(comment, replace = "") # remove emojis
    comment = comment.replace("\n", " ") # there's a bunch a \n for new lines that show up, this removes them
    comment = re.sub(r"\s+", " ", comment).strip() # prevents multiple spaces
    return comment

reddit = praw.Reddit(
    client_id="REMOVED",
    client_secret="QTecEq1zqjE0ymIVC3FvwhBOhox5zw",
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
# found a list of stopwords on https://gist.github.com/sebleier/554280
stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", 
             "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", 
             "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", 
             "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", 
             "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", 
             "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", 
             "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", 
             "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", 
             "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
lemma_comments = [
    token.lemma_ 
    for doc in spacy_doc
    for token in doc
    if not token.is_stop and token.is_alpha]

print(lemma_comments)