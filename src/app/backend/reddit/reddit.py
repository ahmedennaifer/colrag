from dotenv import load_dotenv
import os
import praw
from typing import Iterable, List, Optional, Union
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
load_dotenv()


class RedditScrapper:
    def __init__(self, subreddit: Union[str, None] = None) -> None:
        self.client = praw.Reddit(
            client_id=os.environ["REDDIT_CLIENT_ID"],
            client_secret=os.environ["REDDIT_CLIENT_SECRET"],
            user_agent=os.environ["REDDIT_WEB_AGENT"],
        )
        self.posts: List[praw.reddit.Submission] = []
        self.comments: List[praw.reddit.Comment] = []
        try:
            self.sub = self.client.subreddit(subreddit)
            logger.info(f"Initialized client for sub {subreddit}")
        except Exception as e:
            logger.error(f"Could not init client for sub `{subreddit}`: {e}")

    def get_all_posts_from_subreddit(self) -> Optional[List[praw.reddit.Submission]]:
        try:
            logger.debug(f"getting sub {self.sub}...")
            self.posts = []  # Clear the list first
            for post in self.sub.hot(limit=300):
                if isinstance(post, praw.reddit.Submission):
                    # Only append posts that have either text or title
                    if post.title or post.selftext:
                        logger.debug(
                            f" added post {post.id} with title: {post.title[:50]}..."
                        )
                        self.posts.append(post)
                    else:
                        logger.debug(f"Skipping empty post {post.id}")
                else:
                    logger.error("unrecognized object!")
            logger.info(f"Retrieved {len(self.posts)} posts")
            return self.posts
        except Exception as e:
            logger.error(f"Could not get posts from sub `{self.sub}`: {e}")
            return None

    def get_posts_by_query(
        self, query: str
    ) -> Optional[Iterable[praw.reddit.Submission]]:
        try:
            logger.debug(f"getting info for search query {query} for sub {self.sub}")
            posts = self.sub.search(query, limit=5)
            return list(posts)
        except Exception as e:
            logger.error(
                f"Error getting posts for query {query} for sub {self.sub}: {e}"
            )
            return None

    def get_all_comments_from_subreddit(self) -> Optional[List[praw.reddit.Comment]]:
        try:
            logger.debug(f"getting comments for sub {self.sub}...")
            for post in self.posts:
                post.comments.replace_more(limit=None)
                for comment in post.comments.list():
                    logger.debug(comment.body)
                    if isinstance(comment, praw.reddit.Comment):
                        logger.debug(f" added comment {comment.id}")
                        self.comments.append(comment)
                    else:
                        logger.error("unrecognized object!")
            return self.comments
        except Exception as e:
            logger.error(f"Could not get comments for post `{self.sub}`: {e}")
            return None
