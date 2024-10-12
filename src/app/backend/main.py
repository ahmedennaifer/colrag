from fastapi import FastAPI

from .database.db import get_db
from .database.models.user import User
from pydantic import BaseModel, EmailStr

import logging
import colorlog

handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)s:%  (message)s",
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


class UserReq(BaseModel):
    username: str
    email: EmailStr
    password: str


app = FastAPI()


db = next(get_db())


@app.post("/send_user")
async def root(usr: UserReq):
    user_dict = {"username": usr.username, "email": usr.email, "password": usr.password}
    user = User(**user_dict)
    try:
        db.add(user)
        db.commit()
        logger.info(
            f"Inserted User with info : Name : {user.username}, Email : {user.email}, {user.password}"
        )
    except Exception as e:
        logger.error(f"Error: {e}")
