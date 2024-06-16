import os

from django.test import SimpleTestCase, TestCase, override_settings
from django.template import Template, Context
from django.templatetags.static import static

from BaseApp.utils import get_parent_folder, get_module_logger, bleach_clean_value, join_paths
from BaseApp.templatetags.button_group_tags import init_toggled_button_groups
from BaseApp.exceptions import TemplateTagInitError


class UtilsTests(SimpleTestCase):
    """
    Test the utility functions in BaseApp.utils
    """

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


class InitToggledButtonGroupsTagTest(TestCase):
    """
    Test the init_toggled_button_groups template tag
    """
    @override_settings(STATIC_URL='/static/')
    def test_correct_initialization_placement(self):
        """Test that the script tag is placed correctly."""
        module_path = static("BaseApp/modules/ToggledButtonGroup.mjs")
        expected_script_tag = f"""
        <script type="module">
            import {{ ToggledButtonGroup }} from "{module_path}";
            ToggledButtonGroup.initAll('example');
        </script>
        """

        template_string = "{% load button_group_tags %}<div id='example-toggled-button-group'>...</div>{% init_toggled_button_groups 'example' %}"
        template = Template(template_string)
        rendered = template.render(Context({}))

        # Remove extra whitespace for comparison
        rendered = ''.join(rendered.split())
        expected_script_tag = ''.join(expected_script_tag.split())

        self.assertIn(expected_script_tag, rendered)

    @override_settings(STATIC_URL='/static/')
    def test_no_argument_raises_error(self):
        """Test that TemplateTagInitError is raised if no arguments are given."""
        template_string = "{% load button_group_tags %}{% init_toggled_button_groups %}"
        template = Template(template_string)

        with self.assertRaises(TemplateTagInitError):
            template.render(Context({}))

    @override_settings(STATIC_URL='/static/')
    def test_reserved_suffix_raises_error(self):
        """Test that TemplateTagInitError is raised if group ID contains reserved suffix."""
        template_string = "{% load button_group_tags %}{% init_toggled_button_groups 'example-toggled-button-group' %}"
        template = Template(template_string)

        with self.assertRaises(TemplateTagInitError):
            template.render(Context({}))

    @override_settings(STATIC_URL='/static/')
    def test_multiple_group_ids_initialization(self):
        """Test that multiple group IDs are initialized correctly."""
        module_path = static("BaseApp/modules/ToggledButtonGroup.mjs")
        expected_script_tag = f"""
        <script type="module">
            import {{ ToggledButtonGroup }} from "{module_path}";
            ToggledButtonGroup.initAll('example1 example2 example3');
        </script>
        """

        template_string = "{% load button_group_tags %}{% init_toggled_button_groups 'example1' 'example2' 'example3' %}"
        template = Template(template_string)
        rendered = template.render(Context({}))

        # Remove extra whitespace for comparison
        rendered = ''.join(rendered.split())
        expected_script_tag = ''.join(expected_script_tag.split())

        self.assertIn(expected_script_tag, rendered)

    @override_settings(STATIC_URL='/static/')
    def test_mixed_valid_and_invalid_group_ids(self):
        """Test that TemplateTagInitError is raised if at least one group ID contains reserved suffix."""
        template_string = "{% load button_group_tags %}{% init_toggled_button_groups 'valid1' 'invalid-toggled-button-group' 'valid2' %}"
        template = Template(template_string)

        with self.assertRaises(TemplateTagInitError):
            template.render(Context({}))

    @override_settings(STATIC_URL='/static/')
    def test_whitespace_in_group_ids(self):
        """Test that group IDs with leading, trailing, and internal whitespace are handled correctly."""
        module_path = static("BaseApp/modules/ToggledButtonGroup.mjs")
        expected_script_tag = f"""
        <script type="module">
            import {{ ToggledButtonGroup }} from "{module_path}";
            ToggledButtonGroup.initAll('example1 example2 example3');
        </script>
        """

        template_string = "{% load button_group_tags %}<div id='example1'>...</div><div id='example2'>...</div><div id='example3'>...</div>{% init_toggled_button_groups '  example1 ' 'example2  ' '  example3  ' %}"
        template = Template(template_string)
        rendered = template.render(Context({}))

        expected_script_tag = expected_script_tag.strip()

        self.assertIn(expected_script_tag, rendered)

    @override_settings(STATIC_URL='/static/')
    def test_invalid_characters_in_group_ids(self):
        """Test that TemplateTagInitError is raised if group ID contains invalid characters."""
        template_string = "{% load button_group_tags %}{% init_toggled_button_groups 'invalid<id' %}"
        template = Template(template_string)

        with self.assertRaises(TemplateTagInitError):
            template.render(Context({}))
