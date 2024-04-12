#!/usr/bin/env python3
"""Encrypting passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password
    """
    hashed = bcrypt.hashpw(
        password.encode(),
        salt=bcrypt.gensalt()
    )
    return hashed


def is_valid(hashed_password, password):
    """Check valid password
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
