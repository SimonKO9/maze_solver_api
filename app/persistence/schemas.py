from pydantic import BaseModel
import typing as t


class User(BaseModel):
    username: str


class UserCreate(User):
    hashed_password: str


class Maze(BaseModel):
    id: str
    entrance: str
    gridSize: str
    walls: t.List[str]

    class Config:
        orm_mode = True


class Token(BaseModel):
    token: str
