from fastapi import FastAPI, HTTPException, Depends
from starlette.responses import JSONResponse

from app.maze.maze_service import MazeService, MazeNotFoundException
from app.maze.maze_solver import MazeException
from app.maze.models import Maze, CreateMazePayload, Steps
from app.user.user_service import UserService, Credentials, AuthException
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
        raise HTTPException(403, str(e))


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
def maze_exception_handler(req, e: MazeException):
    return JSONResponse(
        status_code=500,
        content={'message': e.message}
    )


@app.exception_handler(MazeNotFoundException)
def maze_not_found_exception_handler(req, e):
    return JSONResponse(
        status_code=404,
        content={'message': "Maze not found."}
    )


@app.exception_handler(AuthException)
def auth_exception_handler(req, e: AuthException):
    return JSONResponse(
        status_code=403,
        content={'message': e.message}
    )
