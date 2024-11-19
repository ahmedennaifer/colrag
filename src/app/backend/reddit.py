from dotenv import load_dotenv
import os
import praw

load_dotenv()


reddit = praw.Reddit(
    client_id=os.environ["REDDIT_CLIENT_ID"],
    client_secret=os.environ["REDDIT_CLIENT_SECRET"],
    user_agent="web-app v1.0 by /u/	Relevant-Insect49",
)

sub = reddit.subreddit("Python")

all_submissions = []
post_id = "1gu7g70"
submission = reddit.submission(id=post_id)

print(submission.title)
