#!/usr/bin/env python3
"""Auth Module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class to manage the API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Define which routes don't need authentication
        Returns:
        - True if the path is not in the list of strings excluded_paths
        - True if path is None
        - True if excluded_paths is None or empty
        - False if path is in excluded_paths
        """
        if any([path is None, excluded_paths is None]):
            return True
        if len(excluded_paths) == 0:
            return True
        if not path.endswith('/'):
            path += '/'

        if path in excluded_paths:
            return True
        else:
            return False

    def authorization_header(self, request=None) -> str:
        """Public Method
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Public method
        """
        return None
