#!/usr/bin/python3
""" Defines unittests for models/base_model.py."""
import os
import pep8
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestBaseModel(unittest.TestCase):
    """tests  the BaseModel class"""

    @classmethod
    def setUpClass(cls):
        """
        Set up testing environment.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.storage = FileStorage()
        cls.base = BaseModel()

    @classmethod
    def tearDownClass(cls):
        """
        Teardown testing environment.

        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.storage
        del cls.base

    def test_pep8_conformance(self):
        """Test that we conform to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files("models/base_model.py")
        self.assertEqual(result.total_errors, 0, "Fix pep8")

    def test_docstring(self):
        """test if docstring"""
        self.assertIsNotNone(BaseModel.__doc__)

    def test_attr(self):
        """Check for BaseModel attributes."""
        self.assertEqual(str, type(self.base.id))
        self.assertEqual(datetime, type(self.base.created_at))
        self.assertEqual(datetime, type(self.base.updated_at))

    def test_allmethods(self):
        """Check for all methods."""
        self.assertTrue(hasattr(BaseModel, "__init__"))
        self.assertTrue(hasattr(BaseModel, "save"))
        self.assertTrue(hasattr(BaseModel, "to_dict"))
        self.assertTrue(hasattr(BaseModel, "delete"))
        self.assertTrue(hasattr(BaseModel, "__str__"))

    def test_init(self):
        """Test init method."""
        self.assertIsInstance(self.base, BaseModel)

    def test_unique(self):
        """Test unique id."""
        bm = BaseModel()
        self.assertNotEqual(self.base.id, bm.id)
        self.assertLess(self.base.created_at, bm.created_at)
        self.assertLess(self.base.updated_at, bm.updated_at)

    @unittest.skipIf(os.getenv("HBNB_ENV") is not None, "Testing DBStorage")
    def test_save(self):
        """Test save method."""
        self.base.save()
        self.assertNotEqual(self.base.created_at, self.base.updated_at)
        self.assertTrue(os.path.isfile("file.json"))
        with open("file.json", "r") as f:
            self.assertIn("BaseModel.{}".format(self.base.id), f.read())

    def test_to_dict(self):
        """Test to_dict method."""
        testDict = self.base.to_dict()
        self.assertEqual(self.base.id, testDict["id"])
        self.assertEqual(self.base.created_at.isoformat(),
                         testDict["created_at"])
        self.assertEqual(self.base.updated_at.isoformat(),
                         testDict["updated_at"])
        self.assertEqual("__class__", testDict.keys())
        self.assertEqual("BaseModel", testDict["__class__"])
        self.assertEqual(testDict.get("_sa_instance_state", None), None)

    def test_str(self):
        """Test __str__ method."""
        teststr = self.base.__str__()
        self.assertIn("[BaseModel] ({})".format(self.base.id), teststr)
        self.assertIn("'id': '{}'".format(self.base.id), teststr)
        self.assertIn("'created_at': {}".format(
            repr(self.base.created_at)), teststr)
        self.assertIn("'updated_at': {}".format(
            repr(self.base.updated_at)), teststr)
