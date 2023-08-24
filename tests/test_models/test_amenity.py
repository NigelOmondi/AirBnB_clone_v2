#!/usr/bin/python3
""" Defines tests for amenity object"""
import os
import pep8
import models
import MySQLdb
import unittest
from datetime import datetime
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker


class test_Amenity(unittest.TestCase):
    """Tests for amenity class"""
    @classmethod
    def setUpClass(cls):
        """
        Setups amenity for tests
        """
        try:
            os.rename("file.json", "tempo")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.filestorage = FileStorage()
        cls.amenity = Amenity(name="Pool Party")

        if type(models.storage) == DBStorage:
            cls.dbstorage = DBStorage()
            Base.metadata.create_all(cls.dbstorage._DBStorage__engine)
            Session = sessionmaker(bind=cls.dbstorage._DBStorage__engine)
            cls.dbstorage._DBStorage__session = Session()

    @classmethod
    def tearDownClass(cls):
        """Amenity testing teardown.
        Restore original file.json.
        Delete the FileStorage, DBStorage and Amenity test instances.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tempo", "file.json")
        except IOError:
            pass
        del cls.amenity
        del cls.filestorage
        if type(models.storage) == DBStorage:
            cls.dbstorage._DBStorage__session.close()
            del cls.dbstorage

    def test_attr(self):
        """Tests for amenity attributes"""
        testAmenity = Amenity(email="test@gmail.com", password="testpass")
        self.assertEqual(str, type(test_Amenity.id))
        self.assertEqual(datetime, type(test_Amenity.created_at))
        self.assertEqual(datetime, type(test_Amenity.updated_at))
        self.assertEqual(str, type(test_Amenity.name))
        self.assertTrue(hasattr(test_Amenity, "__tablename__"))
        self.assertTrue(hasattr(test_Amenity, "name"))
        self.assertEqual("amenities", test_Amenity.__tablename__)
        self.assertTrue(hasattr(test_Amenity, "place_amenities"))

    def test_pep8(self):
        """Tests for pep8"""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(["models/amenity.py"])
        self.assertEqual(result.total_errors, 0, "fix pep8")

    def test_docstring(self):
        """Tests for docstring in amenity calss"""
        self.assertIsNotNone(Amenity.__doc__)
        self.assertIsNotNone(Amenity.__init__.__doc__)
        self.assertIsNotNone(Amenity.__str__.__doc__)
        self.assertIsNotNone(Amenity.save.__doc__)
        self.assertIsNotNone(Amenity.to_dict.__doc__)

    """Tests incase of DbStorage"""

    unittest.skipIf(type(models.storage) == DBStorage,
                    "Testing DBStorage, not FileStorage")

    def test_save(self):
        """Tests for save method"""
        prevUpdate = self.amenity.updated_at
        self.amenity.save()
        self.assertNotEqual(self.amenity.created_at, self.amenity.updated_at)
        self.assertTrue(os.path.isfile('file.json'))
        self.assertNotEqual(prevUpdate, self.amenity.updated_at)
        with open('file.json', 'r') as f:
            self.assertIn("Amenity." + self.amenity.id, f.read())

    unittest.skipIf(type(models.storage) == DBStorage,
                    "Testing DBStorage, not FileStorage")

    def test_nullable_check(self):
        """Tests for nullable"""
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(Amenity(password="ame"))
            self.dbstorage._DBStorage__session.commit()
            self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(Amenity(email="ame"))
            self.dbstorage._DBStorage__session.commit()

    def test_subclass(self):
        """Check that self is subclass of BaseModel."""
        self.assertTrue(issubclass(Amenity, BaseModel))

    def test_uniqueness(self):
        """Test that different Amenity instances are unique."""
        us = Amenity(email="a", password="a")
        self.assertNotEqual(self.amenity.id, us.id)
        self.assertLess(self.amenity.created_at, us.created_at)
        self.assertLess(self.amenity.updated_at, us.updated_at)

    def test_initialisatio(self):
        """Test initialization of amenity"""
        self.assertIsInstance(self.amenity, Amenity)

    def test_arguments(self):
        """Test initialization with aarguments(args and kwargs)"""
        dt = datetime.utcnow()
        st = Amenity("1", id="69", created_at=dt.isoformat())
        self.assertEqual(st.id, "69")
        self.assertEqual(st.created_at, dt)

    def test_str(self):
        """Test _string rep of class"""
        s = self.amenity.__str__()
        self.assertIn("[Amenity] ({})".format(self.amenity.id), s)
        self.assertIn("'id': '{}'".format(self.amenity.id), s)
        self.assertIn("'created_at': {}".format(
            repr(self.amenity.created_at)), s)
        self.assertIn("'updated_at': {}".format(
            repr(self.amenity.updated_at)), s)
        self.assertIn("'name': '{}'".format(self.amenity.name), s)

    def test_to_dict(self):
        """Test conversion of amenity attributes to dictionary for json"""
        s = self.amenity.to_dict()
        self.assertEqual(s["__class__"], "Amenity")
        self.assertEqual(type(s["created_at"]), str)
        self.assertEqual(type(s["updated_at"]), str)
        fmt = "%Y-%m-%dT%H:%M:%S.%f"
        self.assertEqual(s["created_at"],
                         self.amenity.created_at.strftime(fmt))
        self.assertEqual(s["updated_at"],
                         self.amenity.updated_at.strftime(fmt))
        self.assertEqual(s["name"], self.amenity.name)
        self.assertEqual(s["id"], self.amenity.id)
        self.assertEqual(s["created_at"], self.amenity.created_at.isoformat())
        self.assertEqual(s["updated_at"], self.amenity.updated_at.isoformat())

        unittest.skipIf(type(models.storage) == FileStorage,
                        "Testing FileStorage, not DBStorage")

        def test_save_db(self):
            """Test save method with DBStorage"""
            self.amenity.save()
            self.assertNotEqual(self.amenity.created_at,
                                self.amenity.updated_at)
            self.assertTrue(os.path.isfile('file.json'))
            with open('file.json', 'r') as f:
                self.assertIn("Amenity." + self.amenity.id, f.read())
