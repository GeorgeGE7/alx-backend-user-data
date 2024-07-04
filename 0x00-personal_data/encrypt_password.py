#!/usr/bin/env python3
"""Module for hashing and validating passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password and returns the hashed password as bytes"""
    hashed_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_pass


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if a password matches a hashed password"""
    checked_pass = bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    return checked_pass

