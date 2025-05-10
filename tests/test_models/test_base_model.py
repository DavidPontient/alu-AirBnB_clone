#!/usr/bin/python3
"""Unit tests for BaseModel class."""

import unittest
from models.base_model import BaseModel
from datetime import datetime


class TestBaseModel(unittest.TestCase):
    """Test cases for the BaseModel class."""

    def test_instantiation_without_args(self):
        """Test creating a new BaseModel instance without arguments."""
        model = BaseModel()
        self.assertIsInstance(model.id, str)
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)

    def test_instantiation_with_kwargs(self):
        """Test creating a new BaseModel instance from to_dict() representation."""
        bm1 = BaseModel()
        bm1_dict = bm1.to_dict()
        bm2 = BaseModel(**bm1_dict)

        self.assertEqual(bm1.id, bm2.id)
        self.assertEqual(bm1.created_at, bm2.created_at)
        self.assertEqual(bm1.updated_at, bm2.updated_at)
        self.assertIsInstance(bm2.created_at, datetime)
        self.assertIsInstance(bm2.updated_at, datetime)

    def test_to_dict_contains_expected_keys(self):
        """Test if to_dict contains the right keys and formatted timestamps."""
        model = BaseModel()
        model_dict = model.to_dict()

        self.assertIn("id", model_dict)
        self.assertIn("created_at", model_dict)
        self.assertIn("updated_at", model_dict)
        self.assertIn("__class__", model_dict)
        self.assertEqual(model_dict["__class__"], "BaseModel")
        self.assertIsInstance(model_dict["created_at"], str)
        self.assertIsInstance(model_dict["updated_at"], str)

    def test_str_representation(self):
        """Test __str__ method output."""
        model = BaseModel()
        output = str(model)
        self.assertIn("[BaseModel]", output)
        self.assertIn(model.id, output)


if __name__ == '__main__':
    unittest.main()
