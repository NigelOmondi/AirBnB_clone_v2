#!/usr/bin/python3
"""
Unittests for Reviews class.
"""
import unittest
from os
import pep8
from tests.test_models.test_base_model import test_basemodel
from models.review import Review
from models.base_model import BaseModel


class TestReview(unittest.TestCase):
    """Test the Review class"""

    @classmethod
    def setUpClass(cls):
        """Test set up"""
        cls.review = Review()
        cls.review.place_id = "locationx"
        cls.review.user_id = "guest10"
        cls.review.text = "I highly recommended this place"

    @classmethod
    def teardown(cls):
        """
        To clean up after test is complete
        Deleting "review" attribute from class
        so as to reset test related review/data.
        """
        del cls.review

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
        p = style.check_files(['models/review.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_checking_for_docstring_Review(self):
        """Check for docstrings"""
        self.assertIsNotNone(Review.__doc__)

    def test_attributes_review(self):
        """Check whether Review has attributes"""
        self.assertTrue('id' in self.review.__dict__)
        self.assertTrue('created_at' in self.review.__dict__)
        self.assertTrue('updated_at' in self.review.__dict__)
        self.assertTrue('place_id' in self.review.__dict__)
        self.assertTrue('text' in self.review.__dict__)
        self.assertTrue('user_id' in self.review.__dict__)

    def test_is_subclass_Review(self):
        """Test if review is a subclass of BaseModel"""
        self.assertTrue(issubclass(self.review.__class__, BaseModel), True)

    def test_attribute_types_Review(self):
        """Test attribute type for Review"""
        self.assertEqual(type(self.review.text), str)
        self.assertEqual(type(self.review.place_id), str)
        self.assertEqual(type(self.review.user_id), str)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'DB')
    def test_save_Review(self):
        """test if the save works"""
        self.review.save()
        self.assertNotEqual(self.review.created_at, self.review.updated_at)

    def test_to_dict_Review(self):
        """Test if the dictionary works"""
        self.assertEqual('to_dict' in dir(self.review), True)


if __name__ == "__main__":
    unittest.main()
