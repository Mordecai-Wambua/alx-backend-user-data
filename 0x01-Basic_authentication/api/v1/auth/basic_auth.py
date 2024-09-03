#!/usr/bin/env python3
"""Class to perform Basic Authentication."""
from .auth import Auth


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
