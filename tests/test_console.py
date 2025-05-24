#!/usr/bin/python3
"""Unit tests for FileStorage and BaseModel."""
import unittest
import os
import json
from datetime import datetime
from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """Test cases for the FileStorage class."""

    def setUp(self):
        """Set up test environment."""
        self.file_path = "file.json"
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass
        storage._FileStorage__objects = {}

    def tearDown(self):
        """Tear down test environment."""
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass
        storage._FileStorage__objects = {}

    def test_instance_creation(self):
        """Correct output - instance creation"""
        model = BaseModel()
        self.assertIsInstance(model, BaseModel)

    def test_file_path_type(self):
        """Correct output - type __file_path"""
        self.assertIsInstance(storage._FileStorage__file_path, str)

    def test_objects_type(self):
        """Correct output - type __objects"""
        self.assertIsInstance(storage._FileStorage__objects, dict)

    def test_all_method(self):
        """Correct output - method all()"""
        self.assertIs(storage.all(), storage._FileStorage__objects)

    def test_new_method(self):
        """Correct output - method new()"""
        model = BaseModel()
        key = f"{model.__class__.__name__}.{model.id}"
        self.assertIn(key, storage.all())

    def test_save_method(self):
        """Correct output - method save()"""
        model = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists(self.file_path))

    def test_reload_method(self):
        """Correct output - method reload()"""
        model = BaseModel()
        model.name = "test"
        storage.save()
        storage._FileStorage__objects = {}
        storage.reload()
        key = f"{model.__class__.__name__}.{model.id}"
        self.assertIn(key, storage.all())

    def test_reload_save_reload_flow(self):
        """Correct output - reload() + save() + reload()"""
        model = BaseModel()
        model.name = "test"
        storage.save()
        storage._FileStorage__objects = {}
        storage.reload()
        key = f"{model.__class__.__name__}.{model.id}"
        self.assertIn(key, storage.all())
        storage.save()
        storage.reload()
        self.assertIn(key, storage.all())

    def test_reloaded_objects_match(self):
        """Correct output - reloaded objects are same as created"""
        model = BaseModel()
        model.name = "test"
        model.save()
        model_dict = model.to_dict()
        storage._FileStorage__objects = {}
        storage.reload()
        key = f"{model.__class__.__name__}.{model.id}"
        obj = storage.all()[key]
        self.assertEqual(model.id, obj.id)
        self.assertEqual(model.created_at, obj.created_at)
        self.assertEqual(model.updated_at, obj.updated_at)

    def test_basemodel_created_from_dict(self):
        """Correct output - BaseModel created with dictionary"""
        model = BaseModel()
        model_dict = model.to_dict()
        new_model = BaseModel(**model_dict)
        self.assertEqual(model.id, new_model.id)
        self.assertEqual(model.created_at, new_model.created_at)
        self.assertEqual(model.updated_at, new_model.updated_at)

    def test_file_storage_file_path_exists(self):
        """Test FileStorage: __file_path"""
        self.assertTrue(hasattr(storage, "_FileStorage__file_path"))

    def test_import_storage_with_reload(self):
        """Correct output - from models import storage with reload"""
        from models import storage as test_storage
        self.assertIsInstance(test_storage, FileStorage)
        self.assertTrue(hasattr(test_storage, "reload"))

    def test_file_storage_objects_exists(self):
        """Test FileStorage: __objects"""
        self.assertTrue(hasattr(storage, "_FileStorage__objects"))

    def test_file_storage_all(self):
        """Test FileStorage: all()"""
        self.assertIsInstance(storage.all(), dict)

    def test_file_storage_new(self):
        """Test FileStorage: new()"""
        model = BaseModel()
        key = f"BaseModel.{model.id}"
        self.assertIn(key, storage.all())

    def test_file_storage_save(self):
        """Test FileStorage: save()"""
        model = BaseModel()
        storage.save()
        self.assertTrue(os.path.isfile("file.json"))

    def test_file_storage_reload(self):
        """Test FileStorage: reload()"""
        model = BaseModel()
        model.name = "Reload Test"
        storage.save()
        storage._FileStorage__objects = {}
        storage.reload()
        key = f"{model.__class__.__name__}.{model.id}"
        self.assertIn(key, storage.all())


if __name__ == "__main__":
    unittest.main()
