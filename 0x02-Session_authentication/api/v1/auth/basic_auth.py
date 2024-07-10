#!/usr/bin/env python3
""" Module Basic_auth for user authentication
"""
from typing import TypeVar, Tuple
from base64 import b64decode, decode
from api.v1.auth.auth import Auth
from models.user import User
import base64


class BasicAuth(Auth):
    def decode_base64_authorization_header(self, b64_auth_header: str) -> str:
        """Returns decode base64 authorization"""
        if b64_auth_header is None or not isinstance(b64_auth_header, str):
            return None
        try:
            b64 = base64.b64decode(b64_auth_header)
            b64_decode = b64.decode("utf-8")
        except Exception:
            return None
        return b64_decode

    def extract_user_credentials(self, decoded_b64_auth_header: str) -> (str, str):
        """Returns user credentials"""
        if (
            decoded_b64_auth_header is None
            or not isinstance(decoded_b64_auth_header, str)
            or ":" not in decoded_b64_auth_header
        ):
            return (None, None)
        return decoded_b64_auth_header.split(":", 1)

    """ Extends BasicAuth class
    """

    def extract_base64_authorization_header(self, auth_header: str) -> str:
        """Extract base64 authorization header"""
        if auth_header is None or not isinstance(auth_header, str):
            return None
        if "Basic " not in auth_header:
            return None
        return auth_header[6:]

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar("User"):
        """Returns user object from credentials"""
        if (
            user_email is None
            or not isinstance(user_email, str)
            or user_pwd is None
            or not isinstance(user_pwd, str)
        ):
            return None
        try:
            users = User.search({"email": user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
            return None

    def current_user(self, request=None) -> TypeVar("User"):
        """Overloads Basic authentication"""
        authantication_head = self.authorization_header(request)
        if not authantication_head:
            return None
        base64_exct = self.extract_base64_authorization_header(authantication_head)
        base64_dec = self.decode_base64_authorization_header(base64_exct)
        user_data = self.extract_user_credentials(base64_dec)
        u_login = user_data[0]
        paswd = user_data[1]
        user_data = self.user_object_from_credentials(u_login, paswd)
        return user_data
