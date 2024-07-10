#!/usr/bin/env python3
""" Base module

    Base class, including basic operations
"""
from datetime import datetime
from typing import TypeVar, List, Iterable
from os import path
import json
import uuid


dict_data = {}
time_date_fromat = "%Y-%m-%dT%H:%M:%S"


class Base():
    """ Base class

        Initialize a Base instance
    """

    def __init__(self, *args: list, **kwargs: dict) -> None:
        """ Initialize a Base instance
        """
        instance_class = str(self.__class__.__name__)
        if dict_data.get(instance_class) is None:
            dict_data[instance_class] = {}

        self.id = kwargs.get('id', str(uuid.uuid4()))
        if kwargs.get('created_at') is not None:
            self.created_at = datetime.strptime(kwargs.get('created_at'),
                                                time_date_fromat)
        else:
            self.created_at = datetime.utcnow()
        if kwargs.get('updated_at') is not None:
            self.updated_at = datetime.strptime(kwargs.get('updated_at'),
                                                time_date_fromat)
        else:
            self.updated_at = datetime.utcnow()

    def __eq__(self, other: TypeVar('Base')) -> bool:
        """ Check equality
        """
        if type(self) != type(other):
            return False
        if not isinstance(Base):
            return False
        return (self.id == other.id)

    def to_json(self, for_serialization: bool = False) -> dict:
        """ Convert the object to a JSON dictionary
        """
        result = {}
        for key, value in self.__dict__.items():
            if not for_serialization and key[0] == '_':
                continue
            if type(value) is datetime:
                result[key] = value.strftime(time_date_fromat)
            else:
                result[key] = value
        return result

    @classmethod
    def load_from_file(cls):
        """ Load all objects from file
        """
        instance_class = cls.__name__
        file_path = ".db_{}.json".format(instance_class)
        dict_data[instance_class] = {}
        if not path.exists(file_path):
            return

        with open(file_path, 'r') as f:
            objs_json = json.load(f)
            for obj_id, obj_json in objs_json.items():
                dict_data[instance_class][obj_id] = cls(**obj_json)

    @classmethod
    def save_to_file(cls) -> None:
        """ Save all objects to file
        """
        instance_class = cls.__name__
        file_path = ".db_{}.json".format(instance_class)
        objs_json = {}
        for obj_id, obj in dict_data[instance_class].items():
            objs_json[obj_id] = obj.to_json(True)

        with open(file_path, 'w') as f:
            json.dump(objs_json, f)

    def save(self):
        """ Save current object
        """
        instance_class = self.__class__.__name__
        self.updated_at = datetime.utcnow()
        dict_data[instance_class][self.id] = self
        self.__class__.save_to_file()

    def remove(self):
        """ Remove object
        """
        instance_class = self.__class__.__name__
        if dict_data[instance_class].get(self.id) is not None:
            del dict_data[instance_class][self.id]
            self.__class__.save_to_file()

    @classmethod
    def count(cls) -> int:
        """ Count all objects
        """
        instance_class = cls.__name__
        return len(dict_data[instance_class].keys())

    @classmethod
    def all(cls) -> Iterable[TypeVar('Base')]:
        """ Return all objects
        """
        return cls.search()

    @classmethod
    def get(cls, id: str) -> TypeVar('Base'):
        """ Return one object by ID
        """
        instance_class = cls.__name__
        return dict_data[instance_class].get(id)

    @classmethod
    def search(cls, attributes: dict = {}) -> List[TypeVar('Base')]:
        """ Search all objects with matching attributes
        """
        instance_class = cls.__name__

        def _search(obj):
            if len(attributes) == 0:
                return True
            for k, v in attributes.items():
                if (getattr(obj, k) != v):
                    return False
            return True
        return list(filter(_search, dict_data[instance_class].values()))

