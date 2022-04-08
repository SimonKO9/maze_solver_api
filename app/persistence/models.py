from app.database import Base
from sqlalchemy import Column, ForeignKey, String, ARRAY
from sqlalchemy.orm import relationship
from pydantic import BaseModel


class User(Base):
    __tablename__ = "users"

    username = Column("username", String, primary_key=True, index=True)
    hashed_password = Column("hashed_password", String)

    tokens = relationship("AuthToken", back_populates="owner")
    mazes = relationship("Maze", back_populates="owner")


class AuthToken(Base):
    __tablename__ = "auth_tokens"

    token = Column("token", String, primary_key=True, index=True)
    owner_username = Column("owner_username", String, ForeignKey("users.username"))

    owner = relationship("User", back_populates="tokens")


class Maze(Base):
    __tablename__ = "mazes"

    id = Column("id", String, primary_key=True, index=True)
    entrance = Column("entrance", String)
    gridSize = Column("grid_size", String)
    walls = Column("walls", ARRAY(String))
    owner_username = Column("owner_username", String, ForeignKey("users.username"))

    owner = relationship("User", back_populates="mazes")


