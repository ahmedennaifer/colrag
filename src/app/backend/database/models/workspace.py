from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db import Base


class Workspace(Base):
    __tablename__ = "workspace"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    privacy = Column(String, unique=True, index=False)
    creator_id = Column(Integer, ForeignKey("users.id"))

    documents = relationship("Document", back_populates="workspace")
    users = relationship(
        "User", back_populates="workspaces", secondary="workspace_user"
    )
    creator = relationship("User", back_populates="created_workspaces")


class WorkspaceUser(Base):
    __tablename__ = "workspace_user"
    workspace_id = Column(Integer, ForeignKey("workspace.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
