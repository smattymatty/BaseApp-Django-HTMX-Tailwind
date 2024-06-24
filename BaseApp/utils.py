import os

from functools import wraps
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from loguru import logger
from bleach import clean

from .constants import LOG_FORMAT


def get_parent_folder(path: str):
    """
    Returns the parent folder of a given path.
        - path: The path to get the parent folder of.
    """
    return os.path.dirname(path)


def get_module_logger(module_name: str, file: str):
    """
    Returns a logger for a specific module.
        - module_name: The name of the module.
        - file: The file path to the log file.
    """
    log_file_path = os.path.join(get_parent_folder(
        file), "logs", f"{module_name}.log")
    module_logger = logger.bind(name=module_name)
    module_logger.add(
        log_file_path,
        format=LOG_FORMAT,
        level="DEBUG",
        filter=lambda record: record["extra"].get("name") == module_name,
        rotation="10 MB",
        compression="zip",
    )
    return module_logger


def bleach_clean_value(value):
    """
    Use Bleach to clean the value before saving it to the database.
    This ensures that the value is safe to store in the database.
    """
    cleaned_value = clean(value)
    return cleaned_value


def join_paths(*paths):
    """
    Joins multiple paths into a single path, handling different OS path separators.
    """
    return os.path.join(*paths)


def require_htmx(view_func):
    """
    Decorator to ensure that the view is only accessible via HTMX.
    Example usage:
        @require_htmx(view_func)
        def my_view(request):
            ...
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.htmx:
            return redirect(reverse("BaseApp:home"))
        return view_func(request, *args, **kwargs)
    return _wrapped_view
