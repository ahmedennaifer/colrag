from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from qdrant_client import models

from src.app.backend.database.models.workspace import Workspace
from src.app.backend.database.models.user import User
from src.app.backend.database.models.document import Document
from src.app.backend.auth.utils import get_current_user
from src.app.backend.database.db import get_db
from src.app.backend.database.vector_db import client
from src.app.backend.auth.utils import logger
from src.app.backend.workspaces.models import WorkspaceProperties, WorkspaceReq


router = APIRouter()


@router.post("/create_workspace")
async def create_workspace(
    wrk: WorkspaceReq,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    workspace = Workspace(
        name=wrk.name,
        privacy=wrk.privacy,
        creator_id=current_user.id,
        collection_name=wrk.name,
    )
    try:
        db.add(workspace)
        db.commit()
        logger.info(f"Workspace {workspace.name} created.")
        if client.collection_exists(workspace.collection_name):
            logger.info(f"checking if collection {workspace.collection_name} exists.")
            return {
                "message": f"Collection {workspace.collection_name} already exists."
            }
        else:
            logger.info(f"creating collection {workspace.collection_name}")
            client.create_collection(
                workspace.collection_name,
                vectors_config=models.VectorParams(
                    size=384,
                    distance=models.Distance.COSINE,  # TODO: change to variable param
                ),
            )
            logger.info(f"Collection {workspace.collection_name} created.")
        return {
            "message": f"Workspace {workspace.name} and Collection {workspace.collection_name} created successfully!"
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=400, detail="Workspace creation failed!")


@router.get("/search/{search_query}")
async def search_workspace(search_query: str, db: Session = Depends(get_db)):
    workspaces = db.query(Workspace).filter(Workspace.name.contains(search_query)).all()
    logger.info(workspaces)
    return (
        workspaces
        if workspaces
        else HTTPException(status_code=404, detail="No results found")
    )


@router.get("/get_all")
async def get_workspaces(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    workspaces = (
        db.query(Workspace)
        .filter(or_(Workspace.creator_id == user.id, Workspace.privacy == "public"))
        .all()
    )
    return {
        "workspaces": [
            {"workspace": workspace.name, "type": workspace.privacy}
            for workspace in workspaces
        ]
    }


@router.get("/get_documents")
async def get_all_docs_from_workspace(
    user: Session = Depends(get_current_user),
    db: Session = Depends(get_db),
    properties: WorkspaceProperties = Depends(),
):
    workspace = (
        db.query(Workspace)
        .filter(
            and_(
                Workspace.name == properties.workspace_name,
                Workspace.creator_id == user.id,
            )
        )
        .first()
    )
    if not workspace:
        raise HTTPException(
            status_code=404,
            detail=f"Workspace '{properties.workspace_name}' not found for the current user.",
        )

    docs = db.query(Document).filter(Document.workspace_id == workspace.id).all()

    if docs:
        return {
            "documents": [
                {
                    "document_name": doc.filename,
                    "document_id": doc.id,
                    "workspace_id": doc.workspace_id,
                }
                for doc in docs
            ]
        }

    else:
        raise HTTPException(
            status_code=404,
            detail=f"No documents found in workspace {properties.workspace_name} with id {properties.workspace_id}!",
        )
