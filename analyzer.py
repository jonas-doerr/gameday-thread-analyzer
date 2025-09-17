import praw

reddit = praw.Reddit(
    client_id="REMOVED",
    client_secret="QTecEq1zqjE0ymIVC3FvwhBOhox5zw",
    user_agent="packers_analysis"
)

thread_link = "https://www.reddit.com/r/GreenBayPackers/comments/1neojbv/week_2_game_thread_washington_commanders_green/"
# submission = reddit.submission("1neojbv")
submission = reddit.submission(url=thread_link)
print("fetching comments") #debug in case gets laggy
submission.comments.replace_more(limit=10) #it takes a while if I take too many comments
print("done fetching") #also for debugging purposes
comments = [comment.body for comment in submission.comments.list()[:10]]
print(comments)