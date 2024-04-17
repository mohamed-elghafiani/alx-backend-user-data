#!/usr/bin/env python3
"""Basic Auth module
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


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
        credentials = decoded_base64_authorization_header.split(":")
        email = credentials[0]
        password = ":".join(credentials[1:])
        return email, password

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """returns the User instance based on his email and password.
        Returns:
        - None if user_email is None or not a string
        - None if user_pwd is None or not a string
        - None if the database  doesn’t contain any User
          instance with email equal to user_email
        - None if user_pwd is not the password of the User instance found
        - Otherwise, return the User instance
        """
        if any([user_email is None, not isinstance(user_email, str)]):
            return None
        if any([user_pwd is None, not isinstance(user_pwd, str)]):
            return None
        try:
            users = User.search({"email": user_email})
        except KeyError:
            return None

        if len(users) == 0:
            return None
        user = users[0]
        if user.is_valid_password(user_pwd):
            return user
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves the User instance for a request
        """
        if request is None:
            return None
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        base64_auth = self.extract_base64_authorization_header(auth_header)
        if base64_auth is None:
            return None
        decoded_base64 = self.decode_base64_authorization_header(base64_auth)
        if decoded_base64 is None:
            return None
        email, password = self.extract_user_credentials(decoded_base64)
        if any([email is None, password is None]):
            return None
        user = self.user_object_from_credentials(email, password)
        return user
