from pydantic import BaseModel
from fastapi import Form
from typing import Optional


class DocumentWorkspaceProperties(BaseModel):
    workspace_name: str = Form()
    workspace_id: Optional[int] = Form(None)
