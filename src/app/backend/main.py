from datetime import timedelta, datetime
from typing import Any, Dict
import logging

import colorlog
from fastapi import Depends, FastAPI, HTTPException, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from src.app.backend.database.db import get_db
from src.app.backend.database.models.document import Document
from src.app.backend.database.models.user import User
from src.app.backend.database.models.workspace import Workspace

from .auth.utils import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    verify_password,
    get_current_user,
    get_password_hash,
)

handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)s:%(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )
)
logger = logging.getLogger("fastapi_logger")
logger.setLevel(logging.INFO)
logger.addHandler(handler)


app = FastAPI()


class UserReq(BaseModel):
    username: str
    email: EmailStr
    password: str


class WorkspaceReq(BaseModel):
    name: str
    privacy: str


@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/send_user")
async def get_user(usr: UserReq, db: Session = Depends(get_db)) -> Dict[str, str]:
    user_dict = {
        "username": usr.username,
        "email": usr.email,
        "password": get_password_hash(usr.password),
    }
    user = User(**user_dict)
    try:
        db.add(user)
        db.commit()
        logger.info(f"Inserted User: {user.username}, Email: {user.email}")
        return {"message": "User created successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=400, detail="User creation failed")


@app.post("/send_document")
async def upload_document(
    doc: UploadFile,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    document = Document(
        filename=doc.filename,
        file_path=f"dump/{doc_type}/{doc.filename}",
        file_type=doc_type,
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


@app.post("/workspace")
async def create_workspace(
    wrk: WorkspaceReq,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, str]:
    workspace_dict = {
        "name": wrk.name,
        "privacy": wrk.privacy,
        "creator_id": current_user.id,
    }
    workspace = Workspace(**workspace_dict)
    try:
        db.add(workspace)
        db.commit()
        logger.info(
            f"Workspace with name: {workspace.name} and id: {workspace.id} created successfully!"
        )
        return {"message": f"Workspace {workspace.name} created successfully ! "}
    except Exception as e:
        db.rollback()
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=400, detail="Workspace creation failed!")


@app.get("/get_workspace/{id}")
async def get_workspace_by_id(id: int, db: Session = Depends(get_db)):
    workspace = db.query(Workspace).filter(Workspace.id == id).first()
    if workspace:
        return workspace
    else:
        raise HTTPException(status_code=404, detail=f"Workspace id {id} not found!")


@app.get("/search_workspace/{search_query}")
async def search_workspace(search_query: str, db: Session = Depends(get_db)):
    workspaces = db.query(Workspace).filter(Workspace.name.contains(search_query)).all()
    logger.info(workspaces)
    if workspaces:
        return workspaces
    else:
        raise HTTPException(status_code=404, detail="No results found")


@app.get("/workspaces")
async def get_workspaces(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> Dict[str, Any]:

    workspaces = (
        db.query(Workspace)
        .filter(or_(Workspace.creator_id == user.id, Workspace.privacy == "public"))
        .all()
    )
    if workspaces:
        return {
            "workspaces": [
                {"workspace": workspace.name, "type": workspace.privacy}
                for workspace in workspaces
            ]
        }
    else:
        raise HTTPException(status_code=400, detail="User does not exist!")
