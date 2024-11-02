from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from src.app.backend.database.models.document import Document
from src.app.backend.database.models.user import User
from src.app.backend.auth.utils import get_current_user
from src.app.backend.database.db import get_db
from src.app.backend.auth.utils import logger

router = APIRouter()


@router.post("/send_document")
async def upload_document(
    doc: UploadFile,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    document = Document(
        filename=doc.filename,
        file_path=f"dump/{doc.filename}",
        uploaded_at=datetime.now(),
        user_id=current_user.id,
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
