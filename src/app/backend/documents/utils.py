from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from src.app.backend.database.models.document import Document
from src.app.backend.database.models.workspace import Workspace
from src.app.backend.documents.models import DocumentWorkspaceProperties

# bytesIO for docs (read/write)


def check_existing_document(
    doc: UploadFile,
    db: Session,
    properties: DocumentWorkspaceProperties,
    current_user_id: int,
) -> bool:
    workspace_id = properties.workspace_id
    if not workspace_id and properties.workspace_name:
        workspace = (
            db.query(Workspace)
            .filter(
                Workspace.name == properties.workspace_name,
                Workspace.creator_id == current_user_id,
            )
            .first()
        )
        if not workspace:
            raise HTTPException(
                status_code=404,
                detail=f"Workspace '{properties.workspace_name}' not found for user.",
            )
        workspace_id = workspace.id

    existing_doc = (
        db.query(Document)
        .filter(
            Document.filename == doc.filename,
            Document.workspace_id == workspace_id,
        )
        .first()
    )
    return existing_doc is not None
