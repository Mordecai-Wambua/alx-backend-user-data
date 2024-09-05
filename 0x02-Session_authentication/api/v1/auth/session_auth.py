#!/usr/bin/env python3
"""Session Authentication Class."""
from .auth import Auth
import uuid
from models.user import User


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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID based on a Session ID."""
        if not session_id or not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Return a User instance based on a cookie value."""
        if request:
            cookie_val = self.session_cookie(request)
            user_id = self.user_id_for_session_id(cookie_val)
            return User.get(user_id)
        return None
