import praw

reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="packers_analysis"
)

thread_link = ""
submission = reddit.submission(url=thread_link)
submission.comments.replace_more(limit=0)
comments = [comment.body for comment in submission.comments.list()]