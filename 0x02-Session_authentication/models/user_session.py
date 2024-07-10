#!/usr/bin/env python3
""" User Session Module
"""
from models.base import Base
from typing import TypeVar, List, Iterable
from os import path
import json
import uuid


class UserSession(Base):
    """Users Sessions Class"""

    def __init__(self, *args: list, **kwargs: dict) -> None:
        """Start the user session"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
