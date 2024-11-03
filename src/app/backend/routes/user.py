from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from pydantic import BaseModel, EmailStr

from src.app.backend.database.models.user import User
from src.app.backend.database.models.document import Document
from src.app.backend.auth.utils import get_password_hash, logger
from src.app.backend.database.db import get_db
from src.app.backend.auth.utils import get_current_user


router = APIRouter()


class UserReq(BaseModel):
    username: str
    email: EmailStr
    password: str


@router.post("/send_user")
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


@router.post("/get_all_user_docs")
async def get_all_user_docs(
    user: Session = Depends(get_current_user), db: Session = Depends(get_db)
):
    docs = db.query(Document).filter(Document.user_id == user.id).all()
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
            status_code=404, detail=f"No documents found for user id:{user.id}"
        )
