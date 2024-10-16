from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta

from src.app.backend.database.db import get_db
from src.app.backend.database.models.user import User
from src.app.backend.database.models.document import Document

from .auth.utils import (
    verify_password,
    get_current_user,
    create_access_token,
    get_password_hash,
)


import logging
import colorlog

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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "test"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 2 * 24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


class UserReq(BaseModel):
    username: str
    email: EmailStr
    password: str


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
async def get_user(usr: UserReq, db: Session = Depends(get_db)):
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
    doc_type = doc.filename.split(".")[-1]
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
