#!/usr/bin/env python3
"""Class to perform Basic Authentication."""
from .auth import Auth
import base64


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
                                           str)-> str:
        """Return the decoded value of a Base64 string."""
        if base64_authorization_header:
            if isinstance(base64_authorization_header, str):
                try:
                    x = base64.b64decode(base64_authorization_header,
                                         validate=True)
                except Exception:
                    return None
                return x.decode('utf-8')
