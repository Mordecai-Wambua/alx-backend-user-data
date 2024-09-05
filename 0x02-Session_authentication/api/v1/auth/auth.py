#!/usr/bin/env python3
"""Class to manage the API authentication."""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """Template for all authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determine if path needs authentication."""
        if path and excluded_paths:
            if not path.endswith('/'):
                path += '/'
            for excluded_path in excluded_paths:
                if excluded_path.endswith('*'):
                    if path.startswith(excluded_path[:-1]):
                        return False
                elif path == excluded_path:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Create the necessary header."""
        if request is None:
            return None

        authorization = request.headers.get('Authorization')
        if authorization is None:
            return None

        return authorization

    def current_user(self, request=None) -> TypeVar('User'):
        """Determine the current user."""
        return None

    def session_cookie(self, request=None):
        """Return a cookie value from a request."""
        session_name = getenv('SESSION_NAME')
        if request and session_name:
            return request.cookies.get(session_name)
        return None
