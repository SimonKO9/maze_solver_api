from uuid import uuid4

from app.persistence.persistence import Persistence
from app.persistence.schemas import UserCreate
from app.user.models import User
import hashlib

Credentials = User


class AuthException(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message


class UserAlreadyExistsException(Exception):
    pass


class UserService:

    def __init__(self, persistence: Persistence, salt: str):
        self._persistence = persistence
        self._salt = salt

    def _hash_password(self, password: str) -> str:
        return hashlib.sha512(f"{password}{self._salt}".encode('utf-8')).hexdigest()

    def register(self, user: User):
        existing = self._persistence.get_user_by_username(username=user.username)
        if existing is not None:
            raise UserAlreadyExistsException
        password_hash = self._hash_password(user.password)
        self._persistence.create_user(UserCreate(username=user.username, hashed_password=password_hash))

    # TODO use hash for password
    def login(self, credentials: Credentials):
        password_hash = self._hash_password(credentials.password)
        user = self._persistence.get_user_by_username_and_password(credentials.username, password_hash)
        if user is not None:
            token = str(uuid4())
            self._persistence.create_token(user.username, token)
            return token
        raise AuthException("Invalid credentials.")

    def get_user_for_token_or_throw(self, token: str) -> str:
        user = self._persistence.get_user_for_token(token)
        if user is not None:
            return user.owner_username
        raise AuthException("Invalid token.")
