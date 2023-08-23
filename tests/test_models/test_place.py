#!/usr/bin/python3
"""
unittest for class Place.
"""
import unittest
import os
from tests.test_models.test_base_model import test_basemodel
from models.place import Place
from models.base_model import BaseModel
import pep8


class TestPlace(unittest.TestCase):
    """Test the Place class"""

    @classmethod
    def setUpClass(cls):
        """Test setup"""
        cls.place = Place()
        cls.place.city_id = "County-047"
        cls.place.user_id = "user777"
        cls.place.name = "Mi vida Homes"
        cls.place.description = "Beauty and ambience"
        cls.place.number_rooms = 546
        cls.place.number_bathrooms = 4
        cls.place.max_guest = 895389
        cls.place.price_by_night = 70
        cls.place.latitude = 180.0
        cls.place.longitude = 90.0
        cls.place.amenity_ids = []

    @classmethod
    def teardown(cls):
        """
        To clean up after test is complete
        Deleting "place" attribute from class
        so as to reset test related place/data.           
        """
        del cls.place

    def tearDown(self):
        """
        Is called after each test method.
        Clean up any resources/temporary files
        created during execution of test methods.
        """
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_Place(self):
        """Tests pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/place.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_checking_for_docstring_Place(self):
        """Check for docstrings"""
        self.assertIsNotNone(Place.__doc__)

    def test_attributes_Place(self):
        """Check whether amenity has attributes"""
        self.assertTrue('id' in self.place.__dict__)
        self.assertTrue('created_at' in self.place.__dict__)
        self.assertTrue('updated_at' in self.place.__dict__)
        self.assertTrue('city_id' in self.place.__dict__)
        self.assertTrue('user_id' in self.place.__dict__)
        self.assertTrue('name' in self.place.__dict__)
        self.assertTrue('description' in self.place.__dict__)
        self.assertTrue('number_rooms' in self.place.__dict__)
        self.assertTrue('number_bathrooms' in self.place.__dict__)
        self.assertTrue('max_guest' in self.place.__dict__)
        self.assertTrue('price_by_night' in self.place.__dict__)
        self.assertTrue('latitude' in self.place.__dict__)
        self.assertTrue('longitude' in self.place.__dict__)
        self.assertTrue('amenity_ids' in self.place.__dict__)

    def test_is_subclass_Place(self):
        """Test if Place is subclass of Basemodel"""
        self.assertTrue(issubclass(self.place.__class__, BaseModel), True)

    def test_attribute_types_Place(self):
        """Test the attribute type for Place"""
        self.assertEqual(type(self.place.city_id), str)
        self.assertEqual(type(self.place.user_id), str)
        self.assertEqual(type(self.place.name), str)
        self.assertEqual(type(self.place.description), str)
        self.assertEqual(type(self.place.number_rooms), int)
        self.assertEqual(type(self.place.number_bathrooms), int)
        self.assertEqual(type(self.place.max_guest), int)
        self.assertEqual(type(self.place.price_by_night), int)
        self.assertEqual(type(self.place.latitude), float)
        self.assertEqual(type(self.place.longitude), float)
        self.assertEqual(type(self.place.amenity_ids), list)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'DB')
    def test_save_Place(self):
        """test if the save works"""
        self.place.save()
        self.assertNotEqual(self.place.created_at, self.place.updated_at)

    def test_to_dict_Place(self):
        """test if dictionary works"""
        self.assertEqual('to_dict' in dir(self.place), True)


if __name__ == "__main__":
    unittest.main()
