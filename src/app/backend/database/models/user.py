from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
from ..db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    chat_history = Column(JSON, unique=False, index=False)
    documents = relationship("Document", back_populates="owner")
    created_workspaces = relationship(
        "Workspace", back_populates="creator"
    )  # workspace crées par l'utilisateur
    workspaces = relationship(
        "Workspace", secondary="workspace_user", back_populates="users"
    )  # workspace auxquels le user est abonné
