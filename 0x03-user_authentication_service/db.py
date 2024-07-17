#!/usr/bin/env python3
"""DB Module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initializes a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Private memoized session method (object)
        Never used outside DB class
        """
        if self.__session is None:
            DataBaseSession = sessionmaker(bind=self._engine)
            self.__session = DataBaseSession()
        return self.__session

    def add_user(self, email: str, bcrypt_passwd: str) -> User:
        """Add new user to database
        Returns a User object
        """
        new_u = User(email=email, bcrypt_passwd=bcrypt_passwd)
        self._session.add(new_u)
        self._session.commit()
        return new_u

    def find_user_by(self, **kwargs) -> User:
        """Returns first rrow found in users table
        as filtered by methods input arguments
        """
        body_user_attr = ['id', 'email', 'bcrypt_passwd', 'session_id',
                     'reset_token']
        for key in kwargs.keys():
            if key not in body_user_attr:
                raise InvalidRequestError
        result = self._session.query(User).filter_by(**kwargs).first()
        if result is None:
            raise NoResultFound
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """Use find_user_by to locate the user to update
        Update user's attribute as passed in methods argument
        Commit changes to database
        Raises ValueError if argument does not correspond to user
        attribute passed
        """
        updated_user: User = self.find_user_by(id=user_id)
        body_user_attr: list[str] = ['id', 'email', 'bcrypt_passwd', 'session_id',
                     'reset_token']
        for key, value in kwargs.items():
            if key in body_user_attr:
                setattr(updated_user, key, value)
            else:
                raise ValueError
        self._session.commit()
