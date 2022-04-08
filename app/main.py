import os

from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader
from starlette.responses import JSONResponse

from app.maze.maze_service import MazeService, MazeNotFoundException
from app.maze.maze_solver import MazeException
from app.maze.models import CreateMazePayload, Steps
from app.user.models import User
from app.user.user_service import UserService, Credentials, AuthException, UserAlreadyExistsException
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

from .persistence.persistence import Persistence, SqlAlchemyPersistence

app = FastAPI()
auth = APIKeyHeader(name="X-Token")


def get_persistence():
    return SqlAlchemyPersistence(SessionLocal)


def get_user_service(persistence=Depends(get_persistence)):
    return UserService(persistence, os.getenv('PASSWORD_SALT', '1234567890'))


def get_maze_service(persistence=Depends(get_persistence)):
    return MazeService(persistence)


def get_user(token: str = Depends(auth),
             user_service=Depends(get_user_service)):
    return user_service.get_user_for_token_or_throw(token)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/user")
async def register(user: User, user_service=Depends(get_user_service)):
    user_service.register(user)
    return {'username': user.username}


@app.post("/login")
async def login(credentials: Credentials, user_service=Depends(get_user_service)):
    token = user_service.login(credentials)
    return {'token': token}


@app.get("/maze")
async def get_mazes(user=Depends(get_user), maze_service: MazeService = Depends(get_maze_service)):
    return maze_service.get_mazes(user)


@app.post("/maze")
async def create_maze(payload: CreateMazePayload,
                      user=Depends(get_user),
                      maze_service: MazeService = Depends(get_maze_service)):
    return maze_service.create_maze(payload, user)


@app.get("/maze/{maze_id}/solution")
def get_solution(maze_id: str,
                 steps: Steps,
                 user=Depends(get_user),
                 maze_service: MazeService = Depends(get_maze_service)):
    solution = maze_service.get_maze_solution(user, maze_id, steps)
    return solution


@app.exception_handler(MazeException)
def maze_exception_handler(req, exc: MazeException):  # pylint: disable=unused-argument
    return JSONResponse(
        status_code=500,
        content={'message': exc.message}
    )


@app.exception_handler(MazeNotFoundException)
def maze_not_found_exception_handler(req, exc):  # pylint: disable=unused-argument
    return JSONResponse(
        status_code=404,
        content={'message': "Maze not found."}
    )


@app.exception_handler(AuthException)
def auth_exception_handler(req, exc: AuthException):  # pylint: disable=unused-argument
    return JSONResponse(
        status_code=403,
        content={'message': exc.message}
    )


@app.exception_handler(UserAlreadyExistsException)
def user_already_exists_exception_handler(req, exc: UserAlreadyExistsException):  # pylint: disable=unused-argument
    return JSONResponse(
        status_code=400,
        content={'message': 'User already exists.'}
    )
