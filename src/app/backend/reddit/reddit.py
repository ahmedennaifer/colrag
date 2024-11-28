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
            for post in self.sub.hot(limit=1000):
                if isinstance(post, praw.reddit.Submission):
                    logger.debug(f" added posts {post.id}")
                    self.posts.append(post)
                else:
                    logger.error("unrecognized object!")
            return self.posts
        except Exception as e:
            logger.error(f"Could not get posts from sub `{self.sub}`: {e}")

    def get_posts_by_query(
        self, query: str
    ) -> Optional[Iterable[praw.reddit.Submission]]:
        try:
            logger.debug(f"getting info for search query {query} for sub {self.sub}")
            posts = self.sub.search(query, limit=10)
            return list(posts)
        except Exception as e:
            logger.error(
                f"Error getting posts for query {query} for sub {self.sub}: {e}"
            )

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


if __name__ == "__main__":
    r = RedditScrapper("Python")
    # posts = r.get_all_posts_from_subreddit()
    # comments = r.get_all_comments_from_subreddit()
    q_posts = r.get_posts_by_query("ruff")
    print(len(q_posts))
    print(q_posts[0].comments[0].body)  # 437, 5716


"""
How to model this?
Make a collection from search results?
Make a collection from series of posts?
Make a collection from series of Comments?
"""
