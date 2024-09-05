#!/usr/bin/env python3
"""Session Authentication Class."""
from .auth import Auth
import uuid


class SessionAuth(Auth):
    """Defines the authentication mechanism."""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session Id for a user_id."""
        if not user_id or not isinstance(user_id, str):
            return None
        id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[id] = user_id
        return id
