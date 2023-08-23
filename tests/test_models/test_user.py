#!/usr/bin/python3
""" 
Unittest for User class
"""
import unittest
import os
import pep8
from tests.test_models.test_base_model import test_basemodel
from models.user import User
from models.base_model import BaseModel


class TestUser(unittest.TestCase):
    """Test the User class"""

    @classmethod
    def setUpClass(cls):
        """Test set-up"""
        cls.user = User()
        cls.user.first_name = "Nigel"
        cls.user.last_name = "Omondi"
        cls.user.email = "nigelomondi62@gmail.com"
        cls.user.password = "pa5sw0rd"

    @classmethod
    def teardown(cls):
        """
        To clean up after test is complete
        Deleting "user" attribute from class
        so as to reset test related user/data.  
        """
        del cls.user

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

    def test_pep8_User(self):
        """Tests pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/user.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_checking_for_docstring_User(self):
        """checking for docstrings"""
        self.assertIsNotNone(User.__doc__)

    def test_attributes_User(self):
        """chekcing if User have attributes"""
        self.assertTrue('email' in self.user.__dict__)
        self.assertTrue('id' in self.user.__dict__)
        self.assertTrue('created_at' in self.user.__dict__)
        self.assertTrue('updated_at' in self.user.__dict__)
        self.assertTrue('password' in self.user.__dict__)
        self.assertTrue('first_name' in self.user.__dict__)
        self.assertTrue('last_name' in self.user.__dict__)

    def test_is_subclass_User(self):
        """test if User is subclass of Basemodel"""
        self.assertTrue(issubclass(self.user.__class__, BaseModel), True)

    def test_attribute_types_User(self):
        """test attribute type for User"""
        self.assertEqual(type(self.user.email), str)
        self.assertEqual(type(self.user.password), str)
        self.assertEqual(type(self.user.first_name), str)
        self.assertEqual(type(self.user.first_name), str)

    def test_save_User(self):
        """test if the save works"""
        self.user.save()
        self.assertNotEqual(self.user.created_at, self.user.updated_at)

    def test_to_dict_User(self):
        """test if dictionary works"""
        self.assertEqual('to_dict' in dir(self.user), True)


if __name__ == "__main__":
    unittest.main()
