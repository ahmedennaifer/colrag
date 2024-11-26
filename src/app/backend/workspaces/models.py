from pydantic import BaseModel
from typing import Optional
from fastapi import Form


class WorkspaceReq(BaseModel):
    name: str
    privacy: str
    collection_name: str


class WorkspaceProperties(BaseModel):
    workspace_id: Optional[int] = Form(None)
    workspace_collection_name: Optional[str] = Form(None)
    workspace_name: str = Form()
