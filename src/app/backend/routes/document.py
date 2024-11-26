import os
import tempfile
from io import BytesIO

from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime
import PyPDF2


from src.app.backend.database.models.document import Document
from src.app.backend.database.models.user import User
from src.app.backend.database.models.workspace import Workspace
from src.app.backend.auth.utils import get_current_user
from src.app.backend.database.db import get_db
from src.app.backend.aws.s3.s3_wrapper import S3Wrapper
from src.app.backend.auth.utils import logger
from src.app.backend.documents.utils import check_existing_document
from src.app.backend.documents.models import DocumentWorkspaceProperties
from src.app.backend.pipelines.test_index_pdf import Indexing
from src.app.backend.database.vector_db import get_doc_store

router = APIRouter()


@router.post("/send_document")
async def upload_document(
    doc: UploadFile,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    properties: DocumentWorkspaceProperties = Depends(),
):
    if check_existing_document(
        doc, db=db, properties=properties, current_user_id=current_user.id
    ):
        raise HTTPException(
            status_code=401, detail=f"Document '{doc.filename}' already exists!"
        )

    workspace = None
    if properties.workspace_id:
        workspace = (
            db.query(Workspace)
            .filter(
                Workspace.id == properties.workspace_id,
                Workspace.creator_id == current_user.id,
            )
            .first()
        )
    elif properties.workspace_name:
        workspace = (
            db.query(Workspace)
            .filter(
                Workspace.name == properties.workspace_name,
                Workspace.creator_id == current_user.id,
            )
            .first()
        )

    if not workspace:
        raise HTTPException(
            status_code=404,
            detail=f"Workspace with name '{properties.workspace_name}' not found!",
        )

    document = Document(
        filename=doc.filename,
        file_path=f"dump/{doc.filename}",
        file_type=doc.filename.split(".")[-1],
        uploaded_at=datetime.now(),
        user_id=current_user.id,
        workspace_id=workspace.id,
    )
    sw = S3Wrapper()
    try:
        sw.upload_file(doc, "documentbucket", doc.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    res = sw.get_s3_object("documentbucket", doc.filename)

    fs = res.read()
    pdf = PyPDF2.PdfReader(BytesIO(fs))
    logger.info(f"pdf info: {pdf.metadata}")
    doc_store = get_doc_store(workspace.collection_name)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, doc.filename)

        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(fs)
            logger.info(f"Temp file created at: {temp_file_path}")

        index = Indexing(doc_store, doc.filename)

        index.run_index_pipeline([temp_file_path])

    try:
        db.add(document)
        db.commit()
        logger.info(
            f"Document '{doc.filename}' uploaded by {current_user.email} into workspace '{workspace.name}'"
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
