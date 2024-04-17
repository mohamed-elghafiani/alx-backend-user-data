#!/usr/bin/env python3
"""Basic Auth module
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic Authentication class
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str
        ) -> str:
        """returns the Base64 part of the Authorization header
           for a Basic Authentication
           Returns:
           - None if authorization_header is None
           - None if authorization_header is not a string
           - None if authorization_header doesn’t start by Basic
           - Otherwise, return the value after Basic (after the space)
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if authorization_header.split(" ")[0] != "Basic":
            return None
        else:
            return authorization_header.split(" ")[1]
