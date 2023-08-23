#!/usr/bin/python3
""" Defines tests for city object"""
import os
import pep8
import models
import MySQLdb
import unittest
from datetime import datetime
from models.base_model import Base
from models.base_model import BaseModel
from models.city import City
from models.state import State
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker


class test_City(unittest.TestCase):
    """Tests for city class"""
    @classmethod
    def setUpClass(cls):
        """
        Setups city for tests
        """
        try:
            os.rename("file.json", "tempo")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.filestorage = FileStorage()
        cls.city = City(name="San Francisco1")

        if type(models.storage) == DBStorage:
            cls.dbstorage = DBStorage()
            Base.metadata.create_all(cls.dbstorage._DBStorage__engine)
            Session = sessionmaker(bind=cls.dbstorage._DBStorage__engine)
            cls.dbstorage._DBStorage__session = Session()

    @classmethod
    def tearDownClass(cls):
        """City testing teardown.
        Restore original file.json.
        Delete the FileStorage, DBStorage and City test instances.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tempo", "file.json")
        except IOError:
            pass
        del cls.city
        del cls.filestorage
        if type(models.storage) == DBStorage:
            cls.dbstorage._DBStorage__session.close()
            del cls.dbstorage

    def test_docstring(self):
        """Tests for docstrings"""
        self.assertIsNotNone(City.__doc__)
        self.assertIsNotNone(City.__init__.__doc__)
        self.assertIsNotNone(City.__str__.__doc__)
        self.assertIsNotNone(City.save.__doc__)
        self.assertIsNotNone(City.to_dict.__doc__)

    def test_attr(self):
        """Tests for city attributes"""
        testCity = City()
        self.assertEqual(str, type(testCity.id))
        self.assertEqual(datetime, type(testCity.created_at))
        self.assertEqual(datetime, type(testCity.updated_at))
        self.assertEqual(str, type(testCity.name))

    def test_is_subclass(self):
        """Tests to see if City is a subclass of BaseModel"""
        self.assertTrue(issubclass(City, BaseModel))

    def test_init(self):
        """Tests for proper initialization"""
        self.assertTrue(isinstance(self.city, City))

    def test_to_dict(self):
        """Tests to_dict method"""
        testDict = self.city.to_dict()
        self.assertEqual(dict, type(testDict))
        self.assertTrue('to_dict' in dir(self.city))
        self.assertEqual(self.city.id, testDict["id"])
        self.assertEqual("City", testDict["__class__"])
        self.assertEqual(self.city.created_at.isoformat(),
                         testDict["created_at"])
        self.assertEqual(self.city.updated_at.isoformat(),
                         testDict["updated_at"])
        self.assertEqual(self.city.name, testDict["name"])
        self.assertEqual(self.city.state_id, testDict["state_id"])

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage, not FileStorage")
    def test_save(self):
        """Tests for save method"""
        prevUpdate = self.city.updated_at
        self.city.save()
        self.assertNotEqual(self.city.updated_at, prevUpdate)

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage, not DBStorage")
    def test_save_dbstorage(self):
        """Tests for save method with DBStorage"""
        prevUpdate = self.city.updated_at
        self.city.save()
        self.assertNotEqual(self.city.updated_at, prevUpdate)
        db = MySQLdb.connect(user="hbnb_test",
                             passwd="hbnb_test_pwd",
                             db="hbnb_test_db")
        cursor = db.cursor()
        cursor.execute("SELECT * \
                          FROM `cities` \
                         WHERE BINARY name = '{}'".
                       format(self.city.name))
        query = cursor.fetchall()
        self.assertEqual(1, len(query))
        self.assertEqual(self.city.id, query[0][0])
        cursor.close()

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage, not DBStorage")
    def test_nullable(self):
        """Tests for nullable"""
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(City())
            self.dbstorage._DBStorage__session.commit()
            self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(City(name="City"))
            self.dbstorage._DBStorage__session.commit()
            self.dbstorage._DBStorage__session.rollback()

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage, not DBStorage")
    def test_relationship(self):
        """Tests for relationship"""
        state = State(name="California")
        self.dbstorage._DBStorage__session.add(state)
        self.dbstorage._DBStorage__session.commit()
        city = City(name="San Francisco", state_id=state.id)
        self.dbstorage._DBStorage__session.add(city)
        self.dbstorage._DBStorage__session.commit()
        db = MySQLdb.connect(user="hbnb_test",
                             passwd="hbnb_test_pwd",
                             db="hbnb_test_db")
        cursor = db.cursor()
        cursor.execute("SELECT * \
                          FROM `cities` \
                         WHERE BINARY name = 'San Francisco'")
        query = cursor.fetchall()
        self.assertEqual(1, len(query))
        self.assertEqual(city.id, query[0][0])

    def test_pep8(self):
        """Tests for pep8"""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(["models/city.py"])
        self.assertEqual(result.total_errors, 0, "fix pep8")


if __name__ == "__main__":
    unittest.main()
