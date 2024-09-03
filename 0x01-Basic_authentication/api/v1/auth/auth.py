#!/usr/bin/env python3
"""Class to manage the API authentication."""
from flask import request
from typing import List, TypeVar


class Auth:
    """Template for all authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determine authentication requirements."""
        return False

    def authorization_header(self, request=None) -> str:
        """Create the necessary header."""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Determine the current user."""
        return None
