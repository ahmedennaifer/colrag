import logging
import tempfile
import os
from typing import Any, Dict, Union

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from qdrant_client import models

from src.app.backend.database.vector_db import client, get_doc_store
from src.app.backend.pipelines.test_index_pdf import Indexing
from src.app.backend.reddit.reddit import RedditScrapper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter()


class SubredditModel(BaseModel):
    name: str


class QueryModel(BaseModel):
    query: str


def format_subreddit_posts(subreddit_name, posts):
    formatted_output = f"Subreddit: {subreddit_name}\n\n"
    for idx, post in enumerate(posts, 1):
        user_name = post.get("author", "anonymous_user")
        content = post.get("title", "No Content Provided")
        formatted_output += f"Post {idx} by {user_name}:\n{content}\n\n"
    return formatted_output


@router.post("/get_all_post")
async def get_posts_from_subreddit(sub: SubredditModel):
    rs = RedditScrapper(sub.name)
    try:
        posts = rs.get_all_posts_from_subreddit()
        serialized_posts = [
            {
                "title": post.title,
                "url": post.url,
                "score": post.score,
                "id": post.id,
                "created_utc": post.created_utc,
                "author": str(post.author),
            }
            for post in posts
        ]

        formatted_posts = format_subreddit_posts(sub.name, serialized_posts)

        collection_name = f"Subreddit {sub.name}"

        if not client.collection_exists(collection_name):
            logger.info(f"Creating collection {collection_name}")
            client.create_collection(
                collection_name,
                vectors_config=models.VectorParams(
                    size=384, distance=models.Distance.COSINE
                ),
            )
            logger.info(f"Collection {collection_name} created.")
        else:
            logger.info(f"Collection {collection_name} already exists.")

        doc_store = get_doc_store(collection_name)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, f"{sub.name}_posts.txt")

            with open(temp_file_path, "w") as temp_file:
                temp_file.write(formatted_posts)
                logger.info(f"Temp file created at: {temp_file_path}")
            index = Indexing(doc_store, f"{sub.name}_posts.txt")
            index.run_index_pipeline(temp_file_path)

        return {
            "message": f"Workspace {collection_name} and Collection {collection_name} created successfully!"
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Problem getting posts for subreddit {sub.name}: {e}",
        )


@router.post("/get_posts_by_search")
async def get_posts_by_search(
    sub: SubredditModel, query: QueryModel
) -> Union[Dict[str, Any], None]:
    query_str = query.query
    rs = RedditScrapper(sub.name)
    posts = rs.get_posts_by_query(query_str)
    try:
        serialized_posts = [
            {
                "title": post.title,
                "url": post.url,
                "score": post.score,
                "id": post.id,
                "created_utc": post.created_utc,
                "author": str(post.author) if post.author else None,
            }
            for post in posts
        ]
        return {"posts": serialized_posts}

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Problem getting posts for subreddit {sub.name}: {e} ",
        )
