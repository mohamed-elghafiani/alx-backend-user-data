#!/usr/bin/env python3
"""Auth Module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> bytes:
    """Returns a salted hash of the input password
    """
    password = password.encode('utf-8')
    hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_pw


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
