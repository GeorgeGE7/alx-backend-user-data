#!/usr/bin/env python3
"""Auth class to interact with the authentication database."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from db import DB
from user import User
import bcrypt
import uuid


def _hash_password(password: str) -> str:
    """Hash a password."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a new UUID."""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize a new DB instance."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user."""
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User already exists.")
        except NoResultFound:
            bcrypt_passwd = _hash_password(password)
            new_user = self._db.add_user(email, bcrypt_passwd)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Check if a login is valid."""
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.bcrypt_passwd):
                return True
        except NoResultFound:
            pass
        return False

    def create_session(self, email: str) -> str | None:
        """Create a new session for a user."""
        session_id = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str):# -> Any | None:
        """Get the user associated with a session ID."""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user.email
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy a session."""
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Get a reset password token for a user."""
        new_token = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, reset_token=new_token)
            return new_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str):
        """Update a user's password."""
        if reset_token is None or password is None:
            return None
        try:
            user: User = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        bcrypt_passwd = _hash_password(password)
        self._db.update_user(user.id, bcrypt_passwd=bcrypt_passwd,
                             reset_token=None)

