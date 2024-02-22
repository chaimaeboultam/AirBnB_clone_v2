#!/usr/bin/python3
"""This module instantiates an object of class FileStorage or DBStorage"""

import os
from models.engine.file_storage import FileStorage

# Check the value of HBNB_TYPE_STORAGE environment variable
storage_type = os.getenv('HBNB_TYPE_STORAGE')

if storage_type == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    storage = FileStorage()

# Reload the storage data
storage.reload()

