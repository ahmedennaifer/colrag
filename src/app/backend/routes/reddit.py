import logging
import tempfile
import os
from typing import Any, Dict, Union
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from qdrant_client import models

from src.app.backend.database.vector_db import client, get_doc_store
from src.app.backend.pipelines.reddit_retrieval_pipeline import Indexing, Query
from src.app.backend.reddit.reddit import RedditScrapper
from src.app.backend.workspaces.models import WorkspaceProperties, WorkspaceReq
from src.app.backend.database.models.workspace import Workspace
from src.app.backend.database.models.user import User
from src.app.backend.auth.utils import get_current_user
from src.app.backend.database.db import get_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter()


class Message(BaseModel):
    collection_name: str
    message: str

class SubredditModel(BaseModel):
    name: str

class QueryModel(BaseModel):
    query: str

def format_subreddit_posts(subreddit_name, posts):
    output = ""
    for idx, post in enumerate(posts, 1):
        post_content = f"{post['title']}\n{post['selftext']}" if post.get('selftext') else post['title']
        output += f"Post {idx} : {post_content} : Author: {post['author']}\n"

        if post["comments"]:
            for cidx, comment in enumerate(post["comments"], 1):
                output += f"Comment {cidx} : {comment['body']}\n"
        output += "\n"
    return output

@router.post("/get_all_post")
async def get_posts_from_subreddit(sub: SubredditModel, wrk: WorkspaceReq,  db = Depends(get_db), user= Depends(get_current_user) ):
    rs = RedditScrapper(sub.name)
    try:
        posts = rs.get_all_posts_from_subreddit()
        if not posts:
            raise HTTPException(status_code=404, detail="No posts found")

        serialized_posts = []
        for post in posts:
            comments = []
            try:
                post.comments.replace_more(limit=3)
                for comment in post.comments.list()[:10]:
                    comments.append({
                        "body": comment.body,
                        "author": str(comment.author) if comment.author else "deleted"
                    })
            except Exception as e:
                logger.warning(f"Error fetching comments for post {post.id}: {e}")

            serialized_posts.append({
                "title": post.title,
                "selftext": post.selftext,
                "author": str(post.author),
                "comments": comments
            })

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


        workspace = Workspace(
            name=wrk.name,
            privacy=wrk.privacy,
            creator_id=user.id,
            collection_name=sub.name,
        )
        try:
            db.add(workspace)
            db.commit()
            logger.info(f"Workspace {workspace.name} created.")
        except Exception as e:
            return HTTPException(details=f"Failed to create workspace for subreddit {sub.name}", status=500)

        doc_store = get_doc_store(collection_name)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, f"{sub.name}_posts.txt")
            with open(temp_file_path, "w", encoding='utf-8') as temp_file:
                temp_file.write(formatted_posts)

            index = Indexing(doc_store, f"{sub.name}_posts.txt")
            index.run_index_pipeline(temp_file_path)

        return {
            "message": f"Workspace {collection_name} and Collection {collection_name} created successfully!"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
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
        serialized_posts = []

        for post in posts:
            comments = []
            try:
                post.comments.replace_more(limit=3)
                for comment in post.comments.list()[:10]:
                    comments.append({
                        "body": comment.body,
                        "author": str(comment.author) if comment.author else "deleted"
                    })
            except Exception as e:
                logger.warning(f"Error fetching comments for post {post.id}: {e}")

            serialized_posts.append({
                "title": post.title,
                "selftext": post.selftext,
                "author": str(post.author) if post.author else None,
                "comments": comments
            })

        return {"posts": serialized_posts}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Problem getting posts for subreddit {sub.name}: {e} ",
        )

@router.post("/ask_reddit")
async def send_message(msg: Message) -> Dict[str, Any]:
    try:
        doc_store = get_doc_store(collection_name=msg.collection_name)
        logger.info(f"Got doc store {doc_store} for collection {msg.collection_name}")

        query = Query(doc_store)
        response = query.run_pipeline(msg.message)
        return {"message": response}

    except Exception as e:
        print(e)
