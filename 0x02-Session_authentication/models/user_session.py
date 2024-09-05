#!/usr/bin/env python3
"""Model to have session IDs stored in memory."""
from models.base import Base


class UserSession(Base):
    """Session model class."""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize the instance."""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
