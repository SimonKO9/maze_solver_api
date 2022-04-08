from typing import Dict, Any, Optional
from uuid import uuid4

from app.user.models import User

Credentials = User


class AuthException(Exception):
    def __init__(self, message):
        self.message = message


class UserService:
    users: dict[str, User]
    auth: dict[str, str]

    def __init__(self):
        self.users = {'test': User(username="test", password="passw0rd")}
        self.auth = {'123': 'test'}

    def register(self, user: User):
        if user.username in self.users:
            raise Exception("User already exists.")
        else:
            self.users[user.username] = user

    # TODO use hash for password
    def login(self, credentials: Credentials):
        if credentials.username in self.users and self.users[credentials.username].password == credentials.password:
            token = str(uuid4())
            self.auth[token] = credentials.username
            return token
        else:
            raise AuthException("Invalid credentials.")

    def get_user_for_token_or_throw(self, token: str) -> str:
        if token in self.auth:
            return self.auth[token]
        else:
            raise AuthException("Invalid token.")
