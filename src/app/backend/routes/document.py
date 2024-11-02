from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload
from datetime import datetime

from src.app.backend.database.models.document import Document
from src.app.backend.database.models.user import User
from src.app.backend.database.models.workspace import Workspace
from src.app.backend.auth.utils import get_current_user
from src.app.backend.database.db import get_db
from src.app.backend.auth.utils import logger

router = APIRouter()


@router.post("/send_document")
async def upload_document(
    doc: UploadFile,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    workspace_id: int = None,
):
    document = Document(
        filename=doc.filename,
        file_path=f"dump/{doc.filename}",
        file_type=f"{doc.filename[-3:]}",
        uploaded_at=datetime.now(),
        user_id=current_user.id,
        workspace_id=1,  # TODO: this
    )
    try:
        db.add(document)
        db.commit()
        logger.info(f"Document uploaded by {current_user.email}")
        return {"message": "Document uploaded successfully", "document": doc.filename}
    except Exception as e:
        db.rollback()
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Document upload failed")


@router.get(
    "/get_all"
)  # maybe add decorator to check if doc (or user, workspace etc .., is empty)
async def get_all_docs(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    documents = (
        db.query(Document)
        .filter(Workspace.privacy == "public")
        .filter(Workspace.creator_id == user.id)
        .all()
    )
    if documents:
        return {
            "documents": [{"document": document.filename} for document in documents]
        }
    else:
        raise HTTPException(status_code=404, detail="No documents found!")
