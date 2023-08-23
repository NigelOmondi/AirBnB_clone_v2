#!/usr/bin/python3
"""
Unittest for State class.
"""
import unittest
import os
import pep8
from tests.test_models.test_base_model import test_basemodel
from models.state import State
from models.base_model import BaseModel


class TestState(unittest.TestCase):
    """Test the State class"""

    @classmethod
    def setUpClass(cls):
        """Test set-up"""
        cls.state = State()
        cls.state.name = "NRB"

    @classmethod
    def teardown(cls):
        """
        To clean up after test is complete
        Deleting "state" attribute from class
        so as to reset test related states/data.
        """
        del cls.state

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

    def test_pep8_Review(self):
        """Tests pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/state.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_checking_for_docstring_State(self):
        """Check for docstrings"""
        self.assertIsNotNone(State.__doc__)

    def test_attributes_State(self):
        """Check if State has attributes"""
        self.assertTrue('id' in self.state.__dict__)
        self.assertTrue('created_at' in self.state.__dict__)
        self.assertTrue('updated_at' in self.state.__dict__)
        self.assertTrue('name' in self.state.__dict__)

    def test_is_subclass_State(self):
        """Test if State is a subclass of BaseModel"""
        self.assertTrue(issubclass(self.state.__class__, BaseModel), True)

    def test_attribute_types_State(self):
        """Test attribute type for State"""
        self.assertEqual(type(self.state.name), str)

    def test_save_State(self):
        """Test if save works"""
        self.state.save()
        self.assertNotEqual(self.state.created_at, self.state.updated_at)

    def test_to_dict_State(self):
        """Test if dictionary works"""
        self.assertEqual('to_dict' in dir(self.state), True)


if __name__ == "__main__":
    unittest.main()
