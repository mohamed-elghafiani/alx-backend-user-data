#!/usr/bin/env python3
"""Auth Module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class to manage the API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Public method
        """
        return False

    def authorization_header(self, request=None) -> str:
        """Public Method
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Public method
        """
        return None
