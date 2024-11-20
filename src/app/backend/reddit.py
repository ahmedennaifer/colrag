from dotenv import load_dotenv
import os
import praw
from qdrant_client import QdrantClient
from datetime import datetime

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
comments = submission.comments.list()
comment = reddit.comment(comments[0].body)
print(comment)



client = QdrantClient(url="http://localhost:6333")

# client.create_collection(
#      collection_name="Reddit collection test 2",
#      vectors_config=models.VectorParams(size=100, distance=models.Distance.COSINE),
# )

# client.add(collection_name="Reddit Collection test", documents=comment)
client.get_collection(collection_name="Reddit Collection test 2")
print(client)
