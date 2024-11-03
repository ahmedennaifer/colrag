from pydantic import BaseModel
from typing import Optional
from fastapi import Form


class WorkspaceReq(BaseModel):
    name: str
    privacy: str


class WorkspaceProperties(BaseModel):
    workspace_id: Optional[int] = Form(None)
    workspace_name: str = Form()
