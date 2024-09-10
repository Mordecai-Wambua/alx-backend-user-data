#!/usr/bin/env python3
"""Takes in a password string arguments and returns bytes."""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Return a salted hash of the input password."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
