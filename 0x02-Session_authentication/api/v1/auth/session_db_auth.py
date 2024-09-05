#!/usr/bin/env python3
"""Authentication System based on Session ID stored in a database."""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Authentication class inheriting SessionExpAuth"""

    def create_session(self, user_id=None):
        """Create and store new instance of UserSession."""
        if user_id:
            session_id = super().create_session(user_id)
            instance = UserSession({'user_id': user_id, 'session_id': session_id})
            instance.save()
            UserSession.save_to_file()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """Request UserSession from database and return User ID."""
        if session_id:
            UserSession.load_from_file()
            session = UserSession.search({'session_id': session_id})
            if session:
                obj = session[0]
                expiration = obj.created_at + timedelta(
                    seconds=self.session_duration)
                if expiration > datetime.now():
                    return obj.user_id
        return None

    def destroy_session(self, request=None):
        """Destroy the UserSession."""
        if request:
            if self.session_cookie(request):
                session_id = self.session_cookie(request)
                session = UserSession.search({'session_id': session_id})
                session[0].remove()
                return True
        return False