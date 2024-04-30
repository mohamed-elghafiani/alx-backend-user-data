#!/usr/bin/env python3
"""Auth Module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import uuid


def _hash_password(password: str) -> bytes:
    """Returns a salted hash of the input password
    """
    password = password.encode('utf-8')
    hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_pw


def _generate_uuid() -> str:
    """Returns string repr of a new UUID
    Use uuid module
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register new user
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists.")

        except (NoResultFound, InvalidRequestError):
            hashed_pw = _hash_password(password)
            self._db.add_user(email, hashed_pw)

    def valid_login(self, email: str, password: str) -> bool:
        """validate credentials
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            return False
        except (NoResultFound, InvalidRequestError):
            return False

    def create_session(self, email: str) -> str:
        """Creates a new session for a user.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user is None:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """Takes single session_id string argument
        Returns corresponding User or None
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Takes a single user_id integer srgument
        Returns None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            print(user.id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            return None
