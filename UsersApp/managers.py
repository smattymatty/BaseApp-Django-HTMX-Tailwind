from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth import get_user_model
from BaseApp.utils import get_module_logger


module_logger = get_module_logger("managers", __file__)


class CustomUserManager(BaseUserManager):
    """
    A custom manager for our custom User Model. 
    Handles all of the user creation errors and validation.
    This manager also handles the creation of superusers.
    """
    reserved_usernames = [
        'admin', 'null', 'undefined'
    ]  # only superusers can use these usernames

    def create_user(self,
                    email: str,
                    username: str,
                    password: str = None,
                    superuser: bool = False):
        """
        Creates and returns a new user with the provided email, username, and password.

        Args:
            email (str): The email address for the new user.
            username (str): The username for the new user.
            password (str, optional): The password for the new user. Defaults to None.
            superuser (bool, optional): Flag to indicate if the user is a superuser. Defaults to False.

        Raises:
            ValueError: If the username or email is not provided.
            ValidationError: If the email format is invalid, the email already exists, or the password is the same as the username/email.
            Exception: For any other uncaught exceptions during user creation.

        Returns:
            User: The created user object.
        """
        module_logger.debug(
            f"Creating user with username: {username} and email: {email}"
        )
        try:
            # pre-function error handling
            # different errors based on superuser status
            handle_user_creation_errors(self, email, username, password,
                                        is_superuser=superuser)
            # get the correct email, raise ValidationError if incorrect.
            normalized_email = validate_email_and_username(
                self, email, username)
            user = self.model(
                username=username,
                email=normalized_email,
            )
            user.set_password(password)
            # full_clean runs validation for us before saving
            user.full_clean()
            user.save(using=self._db)

            module_logger.success(
                f"User {username} created successfully."
            )

            return user
        except ValueError as e:
            module_logger.error(
                f"Value Error on creating user: {e}"
            )
            raise e
        except ValidationError as e:
            module_logger.error(
                f"Validation Error on creating user: {e}"
            )
            raise e
        except Exception as e:
            module_logger.error(
                f"Uncaught Error on creating user: {e}"
            )
            raise e

    def create_superuser(self, email, username, password=None):
        """
        Creates and returns a new superuser with the provided email, username, and password.

        Args:
            email (str): The email address for the new superuser.
            username (str): The username for the new superuser.
            password (str, optional): The password for the new superuser. Defaults to None.

        Raises:
            ValueError: If the username or email is not provided.
            ValidationError: If the email format is invalid, the email already exists, or the password is the same as the username/email.
            Exception: For any other uncaught exceptions during superuser creation.

        Returns:
            User: The created superuser object.
        """
        try:
            user = self.create_user(
                username=username,
                email=email,
                password=password,
                superuser=True
            )
            user.is_staff = True
            user.is_superuser = True
            user.save(using=self._db)

            return user
        except ValueError as e:
            module_logger.error(
                f"Value Error on creating superuser: {e}"
            )
            raise e
        except ValidationError as e:
            module_logger.error(
                f"Validation Error on creating superuser: {e}"
            )
            raise e
        except Exception as e:
            module_logger.error(
                f"Uncaught Error on creating superuser: {e}"
            )
            raise e


def validate_email_and_username(manager: CustomUserManager,
                                email: str,
                                username: str) -> str:
    """
    Validates the email and username using regex patterns and normalizes the email.

    Args:
        manager (CustomUserManager): The instance of the CustomUserManager.
        email (str): The email address to be validated.
        username (str): The username to be validated.

    Returns:
        str: The normalized email if validation is successful.

    Raises:
        ValidationError: If the email or username doesn't meet the specified regex criteria.
    """
    custom_email_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$',
        message="Invalid email format"
    )
    custom_email_validator(email)  # Raises ValidationError

    normalized_email: str = manager.normalize_email(email)

    username_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9_-]+$',
        message="Username can only contain letters, numbers, hyphens, and underscores."
    )
    username_validator(username)  # Raises ValidationError

    return normalized_email


def handle_user_creation_errors(manager: CustomUserManager,
                                email: str,
                                username: str,
                                password: str,
                                is_superuser: bool = False):
    """
    Performs pre-validation checks for user creation.

    Args:
        manager (CustomUserManager): The instance of the CustomUserManager.
        email (str): The email address of the user.
        username (str): The username of the user.
        password (str): The password of the user.
        is_superuser (bool, optional): Flag to indicate if the user is a superuser. Defaults to False.

    Raises:
        ValueError: If the username or email is not provided.
        ValidationError: If the email already exists, if the password is the same as the username or email, or if a non-superuser tries to use a reserved username.
    """
    if not username:
        raise ValueError(
            'Users must have a username'
        )
    if not email:
        raise ValueError(
            'Users must have an email address'
        )
    if get_user_model().objects.filter(email=email):
        raise ValidationError(
            ("Email already Exists: %(email)s"),
            params={'email': email},
        )
    if password == username or password == email.split('@')[0]:
        raise ValidationError(
            'Your password should NOT be the same as your username or email!'
        )
    if is_superuser is False:
        if username in manager.reserved_usernames:
            raise ValidationError(
                '%(username)s has been reserved! Pick another one!',
                params={'username': username}
            )
