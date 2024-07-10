#!/usr/bin/env python3
"""
Module provides authentication system for API
"""
from os import getenv
from flask import request
from typing import List


class Auth:
    """
    Class for managing authentication in API
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if path is not in excluded paths

        Args:
            path (str): Path to check
            excluded_paths (List[str]): List of excluded paths

        Returns:
            bool: True if path is not in excluded paths, False otherwise
        """
        if not path or not excluded_paths:
            return True

        path = path.rstrip("/") + "/"
        excluded_paths = [p.rstrip("/") + "/" for p in excluded_paths]

        for excluded_path in excluded_paths:
            if path.startswith(excluded_path):
                return False

        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Get authorization header from request

        Args:
            request: Flask request object

        Returns:
            str: Authorization header value or None
        """
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> object:
        """
        Get current user from request

        Args:
            request: Flask request object

        Returns:
            object: User object or None
        """
        return None

    def session_cookie(self, request=None):  # -> Any | None:
        """
        Get session cookie from request

        Args:
            request: Flask request object

        Returns:
            str: Session cookie value or None
        """
        if request is None:
            return None
        cookie = getenv("SESSION_NAME")
        return request.cookies.get(cookie)
