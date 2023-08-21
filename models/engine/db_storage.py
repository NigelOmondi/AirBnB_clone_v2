#!/usr/bin/python3
"""Represents the relational storage Engine."""

from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.user import User
from models.state import State
from models.review import Review
from models.place import Place
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from os import getenv


class DBStorage:
    """Manages the relational database storage. 
        attr:
            :: __engine: The engine used.
            :: __session: the current open session.    
    """

    __engine = None
    __session = None
    __classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }

    def __init__(self):
        """Creates an engine for access to the database."""

        dbUser = getenv("HBNB_MYSQL_USER")
        dbPasswd = getenv("HBNB_MYSQL_PWD")
        dbHost = getenv("HBNB_MYSQL_HOST")
        dbName = getenv("HBNB_MYSQL_DB")
        dbEnv = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(dbUser, dbPasswd, dbHost,
                                              dbName), pool_pre_ping=True)
        if dbEnv == "test":
            Base.metadata.drop_all(self.__engine)

        def all(self, cls=None):
            """
                Returns a dictionary of all objects of a specific class,
                or all objects if cls is None.

                Args:
                    cls (class object, optional): The class for which to
                    retrieve objects.

                Returns:
                    dict: A dictionary of objects where the keys are in
                    the format "ClassName.object_id".
            """

            objectList = {}

            if cls is not None:
                if isinstance(cls, str):
                    cls = self.__classes.get(cls)
                if cls is not None:
                    clsobjects = self.__session.query(cls).all()
                    for obj in clsobjects:
                        objectList["{}.{}".format(
                            obj.__class__.__name__, obj.id)] = obj
            else:
                for class_name, class_obj in self.__classes.items():
                    clsobjects = self.__session.query(class_obj).all()
                    for obj in clsobjects:
                        objectList["{}.{}".format(
                            obj.__class__.__name__, obj.id)] = obj

            return objectList

        def save(self):
            """Commits all changes of  current database session."""
            self.__session.commit()

        def delete(self, obj=None):
            """Deletes obj from  current database session if not None."""
            if obj:
                self.__session.delete(obj)

        def reload(self):
            """Reloads objects from the database."""

            Base.metadata.create_all(self.__engine)
            Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
            self.__session = scoped_session(Session)
