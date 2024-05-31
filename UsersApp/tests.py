from django.contrib.auth.models import Group

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Profile

User = get_user_model()

# User Model Tests


class UserModelTests(TestCase):

    def test_invalid_email_rejection(self):
        # Test for rejection of invalid email format
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                username='testuser', email='invalidemail', password='password123')

    def test_email_uniqueness(self):
        # Test to ensure email field is unique
        User.objects.create_user(
            username='testuser1', email='test1@example.com', password='password123')
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                username='testuser2', email='test1@example.com', password='password123')

    def test_password_hashing(self):
        # Test that passwords are hashed
        user = User.objects.create_user(
            username='testuser', email='test@example.com', password='password123')
        self.assertNotEqual(user.password, 'password123')

# Profile Model Tests


class UserGroupTest(TestCase):
    def setUp(self):
        # Create the Basic User group if it doesn't exist
        Group.objects.get_or_create(name='Basic User')

    def test_user_in_basic_user_group(self):
        # Create a new user
        user = User.objects.create_user(
            email='testuser@example.com', username='testuser', password='password123')

        # Check if the user is in the Basic User group
        basic_user_group = Group.objects.get(name='Basic User')
        self.assertTrue(basic_user_group in user.groups.all(),
                        "User is not in the Basic User group")


class ProfileModelTests(TestCase):

    def test_profile_creation_on_user_creation(self):
        # Test automatic profile creation when a new User is created
        user = User.objects.create_user(
            username='testuser', email='test@example.com', password='password123')
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_profile_deletion_on_user_deletion(self):
        # Test profile deletion when the User is deleted
        user = User.objects.create_user(
            username='testuser2', email='test@example.com', password='password123')
        user.delete()
        self.assertFalse(Profile.objects.filter(user=user).exists())

# Superuser Tests


class SuperuserTests(TestCase):

    def test_superuser_creation(self):
        # Test superuser creation with appropriate privileges
        superuser = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='password123')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

# Error Handling in User Creation


class UserCreationErrorHandlingTests(TestCase):

    def test_user_creation_without_email(self):
        # Test user creation without an email raises a ValueError
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username='testuser', email=None, password='password123')

    def test_user_creation_without_username(self):
        # Test user creation without an email raises a ValueError
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username=None, email="email@email.com", password='password123')

# Model String Representation Tests


class ModelStringRepresentationTests(TestCase):

    def test_user_str_representation(self):
        # Test the string representation of the User model
        user = User.objects.create_user(
            username='testuser3', email='test@example.com', password='password123')
        self.assertEqual(str(user), user.username)

    def test_profile_str_representation(self):
        # Test the string representation of the Profile model
        user = User.objects.create_user(
            username='testuser4', email='test@example.com', password='password123')
        profile = Profile.objects.get(user=user)
        self.assertEqual(
            str(profile), f"{user.username}'s profile id: {user.id}")

# User Authentication Tests


class UserAuthenticationTests(TestCase):

    def setUp(self):
        # Set up a user for authentication tests
        self.user = User.objects.create_user(
            username='testuser5', email='test@example.com', password='password123')

    def test_user_authentication_with_correct_credentials(self):
        # Test user authentication with correct credentials
        logged_in = self.client.login(
            email='test@example.com', password='password123')
        self.assertTrue(logged_in)

    def test_user_authentication_with_incorrect_credentials(self):
        # Test user authentication with incorrect credentials
        logged_in = self.client.login(
            email='test@example.com', password='wrongpassword')
        self.assertFalse(logged_in)


class UserEdgeCaseTests(TestCase):
    # Email Edge Cases
    def test_valid_unusual_email_formats(self):
        # Testing with valid but unusual email formats
        unusual_emails = [
            "user+something@example.com",
            "user@subdomain.example.com",
            # Add more examples as needed
        ]
        counter = 0
        for email in unusual_emails:
            counter += 1
            with self.subTest(email=email):
                user = User.objects.create_user(
                    username=f'testuser_for_unusual_email{counter}', email=email, password='password123')
                self.assertIsNotNone(user)

    def test_very_long_email_address(self):
        # Testing with an extremely long email address
        long_email = 'a' * 250 + '@example.com'
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                username='testuser', email=long_email, password='password123')

    def test_non_standard_email_characters(self):
        # Testing with technically valid but non-standard email characters
        non_standard_email = 'user&%$#@example.com'
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                username='testuser', email=non_standard_email, password='password123')

    # Username Edge Cases
    def test_unusually_long_username(self):
        # Testing with an unusually long username
        long_username = 'a' * 255  # Adjust length as per your model's constraints
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                username=long_username, email='testedge@example.com', password='password123')

    def test_usernames_with_special_characters(self):
        # Testing usernames with special characters
        special_usernames = ["user!@#", "user name", "😊👍"]
        counter = 0
        for username in special_usernames:
            counter += 1
            with self.subTest(username=username):
                with self.assertRaises(ValidationError):
                    User.objects.create_user(
                        username=username, email=f'test_username_special_chars{counter}@example.com', password='password123')

    def test_reserved_word_usernames(self):
        # Testing with usernames that are reserved words
        reserved_usernames = ["admin", "null", "undefined"]
        counter = 0
        for username in reserved_usernames:
            counter += 1
            with self.subTest(username=username):
                with self.assertRaises(ValidationError):
                    User.objects.create_user(
                        username=username, email=f'test_reserved_users{counter}@example.com', password='password123')

    # Password Edge Cases
    def test_edge_case_passwords(self):
        # Testing with edge case passwords
        edge_case_passwords = ['a' * 255, 'p@ssw0rd!😊', 'passwordin中文']
        counter = 0
        for password in edge_case_passwords:
            counter += 1
            with self.subTest(password=password):
                user = User.objects.create_user(
                    username=f'testuser{counter}', email=f'test_edge_password{counter}@example.com', password=password)
                # Checking password is hashed
                self.assertNotEqual(user.password, password)

    def test_password_same_as_username_or_email(self):
        # Testing when the password is the same as username or email
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                username='same', email='same@example.com', password='same')
