import logging
import tempfile
import os
from typing import Any, Dict, Union, List
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from qdrant_client import models
import wikipedia

from src.app.backend.database.vector_db import client, get_doc_store
from src.app.backend.pipelines.wikipedia_retrieval_pipeline import Indexing, Query
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


class WikipediaArticle(BaseModel):
    title: str


class SearchQuery(BaseModel):
    query: str


def format_wikipedia_content(title: str, content: str) -> str:
    return f"Title: {title}\nContent: {content}\n\n"


@router.post("/get_article")
async def get_wikipedia_article(
    wiki: WikipediaArticle,
    wrk: WorkspaceReq,
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        page = wikipedia.page(title=wiki.title, auto_suggest=False)
        formatted_content = format_wikipedia_content(page.title, page.content)
        collection_name = wiki.title
        vector_collection_name = f"Wikipedia {wiki.title}"

        if not client.collection_exists(vector_collection_name):
            logger.info(f"Creating collection {vector_collection_name}")
            client.create_collection(
                vector_collection_name,
                vectors_config=models.VectorParams(
                    size=384, distance=models.Distance.COSINE
                ),
            )
            logger.info(f"Collection {vector_collection_name} created.")
        else:
            logger.info(f"Collection {vector_collection_name} already exists.")

        workspace = Workspace(
            name=wrk.name,
            privacy=wrk.privacy,
            creator_id=user.id,
            collection_name=collection_name,
        )

        try:
            db.add(workspace)
            db.commit()
            logger.info(f"Workspace {workspace.name} created.")
        except Exception as e:
            raise HTTPException(
                detail=f"Failed to create workspace for article {wiki.title}",
                status_code=500,
            )

        doc_store = get_doc_store(vector_collection_name)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, f"{wiki.title}_content.txt")
            with open(temp_file_path, "w", encoding="utf-8") as temp_file:
                temp_file.write(formatted_content)

            index = Indexing(doc_store, f"{wiki.title}_content.txt")
            index.run_index_pipeline(temp_file_path)

        return {
            "message": f"Workspace {vector_collection_name} and Collection {vector_collection_name} created successfully!"
        }

    except wikipedia.exceptions.DisambiguationError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Multiple matches found for {wiki.title}. Please be more specific.",
        )
    except wikipedia.exceptions.PageError as e:
        raise HTTPException(
            status_code=404, detail=f"Wikipedia article not found: {wiki.title}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Problem getting Wikipedia article {wiki.title}: {str(e)}",
        )


@router.post("/search_wikipedia")
async def search_wikipedia(query: SearchQuery) -> Dict[str, List[Dict[str, str]]]:
    try:
        search_results = wikipedia.search(query.query)
        results = []

        for title in search_results[:5]:
            try:
                page = wikipedia.page(title=title, auto_suggest=False)
                results.append(
                    {
                        "title": page.title,
                        "summary": wikipedia.summary(title, sentences=2),
                        "url": page.url,
                    }
                )
            except (
                wikipedia.exceptions.DisambiguationError,
                wikipedia.exceptions.PageError,
            ):
                continue

        return {"results": results}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Problem searching Wikipedia: {str(e)}",
        )


@router.post("/ask_wikipedia")
async def ask_wikipedia(msg: Message) -> Dict[str, Any]:
    try:
        doc_store = get_doc_store(collection_name=msg.collection_name)
        logger.info(f"Got doc store {doc_store} for collection {msg.collection_name}")

        query = Query(doc_store)
        response = query.run_pipeline(msg.message)
        return {"message": response}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error querying Wikipedia content: {str(e)}"
        )
