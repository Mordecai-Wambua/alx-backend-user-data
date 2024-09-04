#!/usr/bin/env python3
"""Class to perform Basic Authentication."""
from .auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Inherit from Auth."""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Return the Base64 part of the Authorization header."""
        if authorization_header:
            if isinstance(authorization_header, str):
                if authorization_header.startswith('Basic '):
                    y = authorization_header.split(' ')
                    y = str(y[1])
                    return y
        return None

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """Return the decoded value of a Base64 string."""
        if base64_authorization_header:
            if isinstance(base64_authorization_header, str):
                try:
                    x = base64.b64decode(base64_authorization_header,
                                         validate=True)
                    return x.decode('utf-8')
                except Exception:
                    return None
        return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Return the user email and password."""
        if decoded_base64_authorization_header:
            if isinstance(decoded_base64_authorization_header, str):
                if decoded_base64_authorization_header.__contains__(':'):
                    return tuple(
                        decoded_base64_authorization_header.split(':', 1))
        return (None, None)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Return the User instance based on his email and password."""
        if not user_email or not isinstance(user_email, str)\
                or not user_pwd or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
            if not users:
                return None
            user = users[0]
            if not user.is_valid_password(user_pwd):
                return None
            return user
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Overloads Auth and retrieves the User instance for a request."""
        header = self.authorization_header(request)
        if not header:
            return None

        base64_header = self.extract_base64_authorization_header(header)
        if not base64_header:
            return None

        credentials = self.decode_base64_authorization_header(base64_header)
        if not credentials:
            return None

        email, password = self.extract_user_credentials(credentials)
        if not email or not password:
            return None

        user = self.user_object_from_credentials(email, password)
        return user
