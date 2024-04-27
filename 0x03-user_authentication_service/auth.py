#!/usr/bin/env python3
"""Auth Module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Returns a salted hash of the input password
    """
    password = password.encode('utf-8')
    hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_pw
