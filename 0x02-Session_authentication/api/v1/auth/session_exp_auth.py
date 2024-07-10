#!/usr/bin/env python3
"""
Session expiration auth class
This class handles the session expiration auth
It inherits from SessionAuth
"""
from os import getenv
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session expiration auth class"""

    def __init__(self) -> None:
        """
        Initializes the SessionExpAuth class
        It sets the session duration based on the SESSION_DURATION env variable
        If the variable is not set or is not an integer, it defaults to 0
        """
        try:
            self.session_duration = int(getenv("SESSION_DURATION"))
        except Exception as error:
            print(error)
            self.session_duration = 0

    def user_id_for_session_id(self, session_id=None) -> None | str:
        """
        Returns the user id for a given session id
        If the session id is invalid or has expired, it returns None
        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        session_object = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_object["user_id"]
        if "created_at" not in session_object:
            return None
        created_at = session_object["created_at"]
        time_delta = timedelta(seconds=self.session_duration)
        if created_at + time_delta < datetime.now():
            return None
        return session_object["user_id"]

    def create_session(self, user_id=None) -> None | str:
        """
        Creates a new session and returns the session id
        The session id is stored in the user_id_by_session_id dictionary
        with the user_id as the value
        """
        id_of_session = super().create_session(user_id)
        if id_of_session is None:
            return None
        self.user_id_by_session_id[id_of_session] = {
            "user_id": user_id, "created_at": datetime.now()
        }
        return id_of_session

