from sqlalchemy.orm import Session
import typing as t
from . import models, schemas
from ..database import SessionLocal, engine


class Persistence:
    def _get_session(self) -> Session:
        pass

    def create_user(self, user: schemas.UserCreate):
        pass

    def get_user_by_username(self, username: str):
        pass

    def create_maze(self, maze: schemas.Maze, username: str):
        pass

    def get_user_by_username_and_password(self, username: str, password_hash: str):
        pass

    def get_mazes_by_username(self, username: str):
        pass

    def create_token(self, username: str, token: str):
        pass

    def get_user_for_token(self, token: str):
        pass


class SqlAlchemyPersistence(Persistence):

    def __init__(self, session_maker: SessionLocal):
        self._session_maker = session_maker
        self._init_db()

    def _init_db(self):
        models.Base.metadata.create_all(bind=engine)

    def create_user(self, user: schemas.UserCreate):
        with SessionLocal() as db:
            db_user = models.User(username=user.username, hashed_password=user.hashed_password)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user

    def get_user_by_username(self, username: str):
        with SessionLocal() as db:
            db_user = db.query(models.User).filter(models.User.username == username).first()
            return db_user

    def create_maze(self, maze: schemas.Maze, username: str):
        with SessionLocal() as db:
            db_maze = models.Maze(**maze.dict(), owner_username=username)
            db.add(db_maze)
            db.commit()
            db.refresh(db_maze)
            return db_maze

    def get_user_by_username_and_password(self, username: str, password_hash: str):
        with SessionLocal() as db:
            return db.query(models.User).filter(
                models.User.username == username,
                models.User.hashed_password == password_hash
            ).first()

    def get_mazes_by_username(self, username: str):
        with SessionLocal() as db:
            return db.query(models.Maze).filter(models.Maze.owner_username == username).all()

    def create_token(self, username: str, token: str):
        with SessionLocal() as db:
            db_token = models.AuthToken(owner_username=username, token=token)
            db.add(db_token)
            db.commit()
            return token

    def get_user_for_token(self, token: str):
        with SessionLocal() as db:
            return db.query(models.AuthToken).filter(models.AuthToken.token == token).first()


class InMemoryPersistence(Persistence):
    _mazes: t.Dict[str, list[schemas.Maze]]
    _users: dict[str, schemas.UserCreate]
    _auth: dict[str, str]

    def __init__(self) -> None:
        super().__init__()
        self._mazes = {}
        self._auth = {}
        self._users = {}

    def create_user(self, user: schemas.UserCreate):
        if user.username not in self._users:
            self._users[user.username] = user
            return
        raise Exception("Already exists")

    def get_user_by_username(self, username: str):
        if username in self._users:
            return self._users[username]
        return None

    def create_maze(self, maze: schemas.Maze, username: str):
        if username in self._mazes:
            self._mazes[username].append(maze)
        else:
            self._mazes[username] = [maze]

    def get_user_by_username_and_password(self, username: str, password_hash: str):
        if username in self._users and self._users[username].hashed_password == password_hash:
            return self._users[username]
        return None

    def get_mazes_by_username(self, username: str):
        if username in self._mazes:
            return self._mazes[username]
        return []

    def create_token(self, username: str, token: str):
        self._auth[token] = username

    def get_user_for_token(self, token: str):
        if token in self._auth:
            return self._users[self._auth[token]]
        return None
