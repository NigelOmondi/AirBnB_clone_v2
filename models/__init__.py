#!/usr/bin/python3
"""
This module instantiates an object of class FileStorage
    :: if encironment used is db it utileses the relation database 
    :: otherwise it uses the json file storage database 
"""
from os import getenv

storage_type = getenv("HBNB_TYPE_STORAGE")

if storage_type == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()
