#!/usr/bin/env python3
"""Takes in a password string arguments and returns bytes."""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Union


def _hash_password(password: str) -> bytes:
    """Return a salted hash of the input password."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Return a string representation of a new uuid."""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initializes instances of the class."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Create a new user if it does not already exist."""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if the user credentials are valid."""
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            return False
        except Exception:
            return False

    def create_session(self, email: str):
        """Generates an uuid and stores it as the user's session_id."""
        try:
            user = self._db.find_user_by(email=email)
            uuid = _generate_uuid()
            self._db.update_user(user.id, session_id=uuid)
            return user.session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Find a user using the session_id."""
        if session_id:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except Exception:
                return None
        return None

    def destroy_session(self, user_id: int) -> None:
        """Updates the corresponding user’s session ID to None."""
        if user_id:
            self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generate a reset password token."""
        user = self._db.find_user_by(email=email)
        if user:
            self._db.update_user(user.id, reset_token=_generate_uuid())
            return user.reset_token
        else:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Handles user password changes."""
        user = self._db.find_user_by(reset_token=reset_token)
        if user:
            payload = {'hashed_password': _hash_password(password),
                       'reset_token': None}
            self._db.update_user(user.id, **payload)
        raise ValueError
