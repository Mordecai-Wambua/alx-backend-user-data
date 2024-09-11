#!/usr/bin/env python3
"""Takes in a password string arguments and returns bytes."""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """Return a salted hash of the input password."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid():
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
