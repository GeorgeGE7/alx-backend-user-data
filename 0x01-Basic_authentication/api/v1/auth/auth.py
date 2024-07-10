#!/usr/bin/env python3
"""
Class to manage API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """
    Handles API authentication methods
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if path is excluded
        """
        if path is None or excluded_paths is None or not len(excluded_paths):
            return True

        if not path.endswith('/'):
            path += '/'
        if not excluded_paths[-1].endswith('/'):
            excluded_paths += '/'

        firts_last = [path[:-1]
                     for path in excluded_paths if path[-1] == '*']

        for path in firts_last:
            if path in path:
                return False

        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Get authorization header from request
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get current user from request
        """
        return None

