#!/usr/bin/env python3
""" User model """

from models.base import Base
import hashlib


class User(Base):
    """User class"""

    def __init__(self, *args: list, **kwargs: dict) -> None:
        """Initialize a User instance"""
        super().__init__(*args, **kwargs)
        self.email = kwargs.get("email")
        self._password = kwargs.get("_password")
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")

    @property
    def password(self) -> str:
        """Getter of the user's password"""
        return self._password

    def is_valid_password(self, pwd: str) -> bool:
        """Validate a password"""
        if pwd is None or type(pwd) is not str:
            return False
        if self.password is None:
            return False
        pwd_e = pwd.encode()
        return hashlib.sha256(pwd_e).hexdigest().lower() == self.password

    @password.setter
    def password(self, pwd: str) -> None:
        """Setter of a new password: encrypt in SHA256"""
        if pwd is None or type(pwd) is not str:
            self._password = None
        else:
            self._password = hashlib.sha256(pwd.encode()).hexdigest().lower()

    def display_name(self) -> str:
        """Display name of user based on email, first_name, and last_name"""
        if self.email is None and self.first_name is None and self.last_name is None:
            return ""
        if self.first_name is None and self.last_name is None:
            return "{}".format(self.email)
        if self.last_name is None:
            return "{}".format(self.first_name)
        if self.first_name is None:
            return "{}".format(self.last_name)
        else:
            return "{} {}".format(self.first_name, self.last_name)
