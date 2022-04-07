from fastapi import FastAPI, HTTPException, Depends

from app.maze.maze_service import MazeService
from app.maze.models import Maze
from app.user.user_service import UserService, Credentials
from app.user.models import User
from fastapi.security import APIKeyHeader

app = FastAPI()
auth = APIKeyHeader(name="X-Token")

deps = {
    'users': UserService(),
    'mazes': MazeService()
}


def get_user_service():
    return deps['users']


def get_maze_service():
    return deps['mazes']


def get_user(token: str = Depends(auth), user_service=Depends(get_user_service)):
    try:
        return user_service.get_user_for_token_or_throw(token)
    except Exception as e:
        raise HTTPException(401, str(e))


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/user")
async def register(user: User, user_service=Depends(get_user_service)):
    try:
        user_service.register(user)
        return {'username': user.username}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/login")
async def login(credentials: Credentials, user_service=Depends(get_user_service)):
    try:
        token = user_service.login(credentials)
        return {'token': token}
    except Exception as e:
        raise HTTPException(401, str(e))
