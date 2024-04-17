#!/usr/bin/env python3
"""Basic Auth module
"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """Basic Authentication class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """returns the decoded value of a Base64 string
           base64_authorization_header:
        Returns:
        - None if base64_authorization_header is None
        - None if base64_authorization_header is not a string
        - None if base64_authorization_header is not a valid Base64
        - Otherwise, return the decoded value as UTF8 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            encoded = base64_authorization_header.encode('utf-8')
            decoded64 = base64.b64decode(encoded)
            decoded = decoded64.decode('utf-8')
            return decoded
        except (UnicodeDecodeError, TypeError, base64.binascii.Error):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """returns the user email and password from the Base64 decoded value.
        Returns:
        - None, None if decoded_base64_authorization_header is None
        - None, None if decoded_base64_authorization_header is not a string
        - None, None if decoded_base64_authorization_header doesn’t contain:
        - Otherwise, return the user email and the user password
          these 2 values must be separated by a :
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(":")
        return email, password
