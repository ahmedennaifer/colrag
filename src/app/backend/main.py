import botocore.exceptions
from fastapi import FastAPI
from src.app.backend.routes import auth, user, document, workspace, chat, reddit
from src.app.backend.auth.utils import logger
from src.app.backend.aws.s3.s3_wrapper import S3Wrapper

from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware


"""
TODO : add workspace id when inserting doc
TODO : add get_workspace/doc/etc.. by id method to pass in params
TODO : decorator to check if exists and return error else
"""

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

sw = S3Wrapper()


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, tags=["Authentication"])
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(document.router, prefix="/document", tags=["Document"])
app.include_router(workspace.router, prefix="/workspace", tags=["Workspace"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(reddit.router, prefix="/reddit", tags=["Reddit"])

logger.info("Application has started...")
