from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, HTTPException, Form
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from datetime import datetime

from src.app.backend.database.models.document import Document
from src.app.backend.database.models.user import User
from src.app.backend.database.models.workspace import Workspace
from src.app.backend.auth.utils import get_current_user
from src.app.backend.database.db import get_db
from src.app.backend.auth.utils import logger

router = APIRouter()


class DocumentWorkspaceProperties(BaseModel):
    workspace_name: str = Form()
    workspace_id: Optional[int] = Form(None)


@router.post("/send_document")
async def upload_document(
    doc: UploadFile,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    properties: DocumentWorkspaceProperties = Depends(),
):
    workspace = None
    logger.info(properties.workspace_name)
    if properties.workspace_id:
        workspace = (
            db.query(Workspace).filter(Workspace.id == properties.workspace_id).first()
        )
    elif properties.workspace_name:
        workspace = (
            db.query(Workspace)
            .filter(Workspace.name == properties.workspace_name)
            .first()
        )

    else:
        raise HTTPException(
            status_code=404,
            detail=f"Workspace with name {properties.workspace_name} not found!",
        )

    document = Document(
        filename=doc.filename,
        file_path=f"dump/{doc.filename}",
        file_type=f"{doc.filename[-3:]}",
        uploaded_at=datetime.now(),
        user_id=current_user.id,
        workspace_id=workspace.id if workspace else None,
    )
    try:
        db.add(document)
        db.commit()
        logger.info(
            f"Document uploaded by {current_user.email} into workspace: {properties.workspace_name}"
        )
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
        .join(Workspace, Document.workspace_id == Workspace.id)
        .filter(or_(Workspace.privacy == "public", Workspace.creator_id == user.id))
        .all()
    )
    if documents:
        return {
            "documents": [
                {
                    "document name": document.filename,
                    "document id": document.id,
                    "author": document.owner.username,
                    "workspace_name": (
                        document.workspace.name if documents else "No docs"
                    ),
                }
                for document in documents
            ]
        }
    else:
        raise HTTPException(status_code=404, detail="No documents found!")


@router.get("/get_document/{id}")
async def get_doc_by_id(
    id: int, user: Session = Depends(get_current_user), db: Session = Depends(get_db)
):
    document = db.query(Document).filter(User.id == user.id, Document.id == id).first()
    if document:
        return document
    else:
        raise HTTPException(status_code=404, details="No document with id: {id} found ")
