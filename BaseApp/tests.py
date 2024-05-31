from django.core.management import call_command
from django.test import TestCase, RequestFactory, SimpleTestCase
from django.template import Context, Template

from BaseApp.styles import TailwindStyle, register_style
from BaseApp.utils import get_parent_folder, get_module_logger, bleach_clean_value, join_paths

import os


class UtilsTests(SimpleTestCase):

    def test_get_module_logger(self):
        """Test the get_module_logger function to ensure that the logger is properly created and the log file exists"""
        module_name = "test_module"
        test_logger = get_module_logger(module_name, __file__)
        expected_log_file_path = os.path.join(
            get_parent_folder(__file__), "logs", f"{module_name}.log")
        # Check if the log file is created in the correct path
        self.assertTrue(os.path.exists(expected_log_file_path))
        # Log a message to the logger
        test_logger.info("Test message")
        with open(expected_log_file_path, "r") as log_file:
            self.assertIn("Test message", log_file.read())
        # Check if the log file contains the expected message
        with open(expected_log_file_path, "r") as log_file:
            self.assertIn("Test message", log_file.read())
        # Optionally clean up by removing the created log file
        test_logger.remove()
        if os.path.exists(expected_log_file_path):
            os.remove(expected_log_file_path)

    def test_bleach_clean_value(self):
        """Test the bleach_clean_value function to ensure that the value is properly cleaned"""
        dirty_value = "<script>alert('test');</script>"
        clean_value = bleach_clean_value(dirty_value)
        self.assertNotIn("<script>", clean_value)

    def test_join_paths(self):
        """Test the join_paths function to ensure that the paths are properly joined"""
        paths = ["folder", "subfolder", "file.txt"]

        # Check the operating system
        if os.name == 'nt':  # Windows
            expected_output = "folder\\subfolder\\file.txt"
        else:  # UNIX-like systems (Linux, macOS)
            expected_output = "folder/subfolder/file.txt"

        self.assertEqual(join_paths(*paths), expected_output)
