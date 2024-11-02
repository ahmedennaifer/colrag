from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.app.backend.database.models.workspace import Workspace
from src.app.backend.database.models.user import User
from src.app.backend.auth.utils import get_current_user
from src.app.backend.database.db import get_db
from src.app.backend.auth.utils import logger


router = APIRouter()


class WorkspaceReq(BaseModel):
    name: str
    privacy: str


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
    )
    try:
        db.add(workspace)
        db.commit()
        logger.info(f"Workspace {workspace.name} created.")
        return {"message": f"Workspace {workspace.name} created successfully!"}
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
