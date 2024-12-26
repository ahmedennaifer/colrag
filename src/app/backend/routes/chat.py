from typing import Any, Dict

from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException
from src.app.backend.database.vector_db import get_doc_store
from src.app.backend.auth.utils import get_current_user, logger
from src.app.backend.pipelines.test_index_pdf import Query
from src.app.backend.database.models.user import User
from src.app.backend.database.db import get_db
from pydantic import BaseModel

router = APIRouter()


class Message(BaseModel):
    collection_name: str
    message: str


"""
// 1 - get json from db
// 2 - update json with correct counter
// 3 - store new json in db
"""


def get_chat_history(user: Depends(get_current_user), db: Depends(get_db)) -> dict:
    try:
        res = db.query(User).filter(User.id == user.id).first()
        return res.chat_history
    except Exception as e:
        raise HTTPException(
            detail=f"Error getting the chat history: {e}", status_code=404
        )


@router.post("/send_message")
async def send_message(msg: Message) -> Dict[str, Any]:
    try:
        doc_store = get_doc_store(collection_name=msg.collection_name)
        logger.info(f"Got doc store {doc_store} for collection {msg.collection_name}")

        query = Query(doc_store)
        response = query.run_pipeline(msg.message)
        return {"message": response["llm"]["replies"][0]}

    except Exception as e:
        print(e)
