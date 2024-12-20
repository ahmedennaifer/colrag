from typing import Any, Dict

from fastapi import APIRouter
from src.app.backend.database.vector_db import get_doc_store
from src.app.backend.auth.utils import logger
from src.app.backend.pipelines.test_index_pdf import Query

from pydantic import BaseModel
from datetime import datetime

import json

router = APIRouter()


class Message(BaseModel):
    collection_name: str
    message: str
    time: datetime


@router.post("/send_message")
async def send_message(msg: Message) -> Dict[str, Any]:
    try:
        doc_store = get_doc_store(collection_name=msg.collection_name)
        logger.info(f"Got doc store {doc_store} for collection {msg.collection_name}")

        query = Query(doc_store)
        response = query.run_pipeline(msg.message)
        fmt_res = response["llm"]["replies"][0]}
        return {"message": response["llm"]["replies"][0]}

    except Exception as e:
        print(e)
