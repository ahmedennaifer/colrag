from fastapi import FastAPI
from src.app.backend.routes import auth, user, document, workspace
from src.app.backend.auth.utils import logger

from fastapi.security import OAuth2PasswordBearer


"""

TODO : add workspace id when inserting doc
TODO : add get_workspace/doc/etc.. by id method to pass in params

"""

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


app.include_router(auth.router, tags=["Authentication"])
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(document.router, prefix="/document", tags=["Document"])
app.include_router(workspace.router, prefix="/workspace", tags=["Workspace"])


logger.info("Application has started...")
