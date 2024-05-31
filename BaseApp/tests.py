from django.core.management import call_command
from django.test import TestCase, RequestFactory, SimpleTestCase
from django.template import Context, Template

from BaseApp.styles import TailwindStyle, register_style
from BaseApp.menus import nav_items
from BaseApp.utils import get_parent_folder, get_module_logger, bleach_clean_value, join_paths

import os


class UtilsTests(SimpleTestCase):

    def test_get_parent_folder(self):
        """Test the get_parent_folder function to ensure that the parent folder is properly extracted"""
        test_path = "C:\\Users\\example\\project\\file.py"
        expected_output = "C:\\Users\\example\\project"
        self.assertEqual(get_parent_folder(test_path), expected_output)

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


class NavButtonsTemplateTagTest(TestCase):
    def setUp(self):
        # Set up the request factory
        self.factory = RequestFactory()

    def render_template(self, string, context):
        """render the template with your custom template tag"""
        return Template(string).render(Context(context))

    def test_nav_buttons_tag(self):
        """test the nav_buttons template tag"""
        rendered = self.render_template(
            '{% load menu_tags %}{% nav_buttons %}',
            {}
        )

        # Check if the output contains expected strings for each button
        for button_name, options in nav_items.items():
            self.assertIn(button_name, rendered)
            for option in options:
                self.assertIn(option.name, rendered)
                self.assertIn(option.url, rendered)


class GenerateTailwindDummyCommandTest(TestCase):

    def setUp(self):
        '''Register a test-specific style'''
        @register_style(name="test-style")
        class TestStyle(TailwindStyle):  # pylint disable= unused-variable-name
            '''Test style class'''
            classes = "test-class-1 test-class-2"

    def test_generate_tailwind_dummy_with_test_style(self):
        '''Define the expected path of the dummy file'''
        expected_file_path = os.path.join(
            'BaseApp', 'templates', 'BaseApp', 'tailwind_dummy.html')

        # Call the management command
        call_command('tailwind_dummy')

        # Check if the file is created
        self.assertTrue(os.path.exists(expected_file_path))

        # Read the file and check if the test style is included
        with open(expected_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            self.assertIn('test-class-1', content)
            self.assertIn('test-class-2', content)

    def tearDown(self):
        '''Remove the generated dummy file after the test'''
        os.remove(os.path.join('BaseApp', 'templates',
                  'BaseApp', 'tailwind_dummy.html'))
