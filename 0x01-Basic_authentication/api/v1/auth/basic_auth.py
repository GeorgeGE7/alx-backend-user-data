#!/usr/bin/env python3
""" Module Basic_auth for user authentication
"""
from typing import TypeVar, Tuple
from base64 import b64decode, decode
from api.v1.auth.auth import Auth
from models.user import User
import base64


class BasicAuth(Auth):
    """ Extends BasicAuth class
    """

    def extract_base64_authorization_header(self, headers_authantication: str) -> str:
        """
        Extract base64 authorization header
        """
        if headers_authantication is None or not isinstance(headers_authantication, str):
            return None
        if 'Basic ' not in headers_authantication:
            return None
        return headers_authantication[6:]

    def decode_base64_authorization_header(self, b64_headers_authantication: str) -> str:
        """
        Returns decode base64 authorization
        """
        if b64_headers_authantication is None or not isinstance(b64_headers_authantication, str):
            return None
        try:
            b64 = base64.b64decode(b64_headers_authantication)
            b64_decode = b64.decode('utf-8')
        except Exception:
            return None
        return b64_decode

    def extract_user_credentials(
            self, decoded_b64_headers_authantication: str) -> (str, str):
        """
        Returns user credentials
        """
        if decoded_b64_headers_authantication is None or not isinstance(
                decoded_b64_headers_authantication, str) \
           or ':' not in decoded_b64_headers_authantication:
            return (None, None)
        return decoded_b64_headers_authantication.split(':', 1)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns user object from credentials
        """
        if user_email is None or not isinstance(
                user_email, str) or user_pwd is None or not isinstance(
                    user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Overloads Basic authentication
        """
        headers_authantication = self.authorization_header(request)
        if not headers_authantication:
            return None
        exed_base64 = self.extract_base64_authorization_header(headers_authantication)
        de_base64 = self.decode_base64_authorization_header(exed_base64)
        user_data = self.extract_user_credentials(de_base64)
        user_login = user_data[0]
        user_passwd = user_data[1]
        user_data = self.user_object_from_credentials(
            user_login, user_passwd)
        return user_data

