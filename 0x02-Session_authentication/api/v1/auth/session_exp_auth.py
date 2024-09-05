#!/usr/bin/env python3
"""Enable expiration of sessions."""
from .session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Inherit from SessionAuth."""

    def __init__(self):
        """Overload initial constructor."""
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Overload method to create a seession dictionary."""
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = {
                'user_id': user_id, 'created_at': datetime.now()}
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """"""
        if session_id:
            if self.user_id_by_session_id.get(session_id):
                session_dict = self.user_id_by_session_id.get(session_id)
                if self.session_duration <= 0:
                    return session_dict.get('user_id')
                if session_dict.get('created_at'):
                    created_at = session_dict.get('created_at')
                    expiration = created_at + timedelta(
                        seconds=self.session_duration)
                    if expiration > datetime.now():
                        return session_dict.get('user_id')
        return None
