#!/usr/bin/python3
"""Defines a database storage engine"""
from os import getenv
from sqlalchemy import (create_engine)
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """creates dbstorge engine"""
    __engine = None
    __session = None

    def __init__(self):
        """creates a public instance"""
        user = getenv('HBNB_MYSQL_USER')
        passwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query all types of objects on the current db session"""
        obj_dict = {}
        if cls is None:
            for cls in [User, State, City, Amenity, Place, Review]:
                query = self.__session.query(cls).all()
                for obj in query:
                    key = "{}.{}".format(cls.__name__, obj.id)
                    obj_dict[key] = obj
        else:
            query = self.__session.query(cls).all()
            for obj in query:
                key = "{}.{}".format(cls.__name__, obj.id)
                obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session"""
        if obj is not None:
            self.session.delete(obj)

    def reload(self):
        """configuration"""
        Base.metadata.create_all(self.__engine)
        sessmake = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sessmake)
        self.__session = Session()

    def close(self):
        """ calls remove()
        """
        self.__session.close()
