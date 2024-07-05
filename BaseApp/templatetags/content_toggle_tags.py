import re
from django import template
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from BaseApp.exceptions import TemplateTagInitError
from BaseApp.utils import get_module_logger

module_logger = get_module_logger("templatetags", __file__)

register = template.Library()

VALID_TOGGLE_ID_PATTERN = re.compile(r'^[a-zA-Z0-9_\-]+$')


@register.simple_tag(takes_context=True)
def init_content_toggles(context, *toggle_ids):
    module_logger.debug(
        f"init_content_toggles tag generated JavaScript code: toggle_ids: {toggle_ids}")
    toggle_ids = [str(toggle_id).strip()
                  for toggle_id in toggle_ids if toggle_id]
    reserved_suffix = "-toggle-container"
    if not toggle_ids:
        raise TemplateTagInitError(
            "init_content_toggles tag requires at least one content toggle ID.", reserved_suffix
        )
    for toggle_id in toggle_ids:
        if reserved_suffix in toggle_id:
            raise TemplateTagInitError(
                f"Invalid toggle ID '{toggle_id}'.", reserved_suffix
            )
        if not VALID_TOGGLE_ID_PATTERN.match(toggle_id):
            raise TemplateTagInitError(
                f"Toggle ID '{toggle_id}' contains invalid characters. Only alphanumeric characters, hyphens, and underscores are allowed.", reserved_suffix
            )
    context['CONTENT_TOGGLES_INITIALIZED'] = True

    module_path = static("BaseApp/modules/ContentToggleHandler.mjs")
    js_code = f"""
        <script type="module">
            import {{ ContentToggleHandler }} from "{module_path}";
            ContentToggleHandler.initAll('{ " ".join(toggle_ids) }');
        </script>
    """

    # TODO: Add further validation for the toggle_ids parameters as needed
    # TODO: Ensure that the toggle_ids exist in the document before proceeding
    # TODO: Consider adding settings to handle different types of toggles and strategies
    # TODO: Add support for adding custom attributes or options in the generated JavaScript code
    # TODO: Add support for dynamically binding toggle events to newly added DOM elements
    # TODO: Load configurations based on the environment (e.g., different configurations for development, staging, production)
    # TODO: Allow users to define custom toggles and events through the Django settings
    # TODO: Implement template inheritance for content_toggle_tags configurations to allow sharing common configurations across templates
    # TODO: Add a debug mode to log detailed information about the initialization process and toggle actions
    # TODO: Integrate performance monitoring to log the execution time of toggle actions and event handlers
    # TODO: Add support for preserving the state of toggles across page reloads (e.g., using localStorage or sessionStorage)
    # TODO: Ensure the generated JavaScript code is accessible and follows best practices (e.g., ARIA roles, keyboard navigation)
    # TODO: Add support for internationalization to handle different languages and locales
    # TODO: Implement enhanced logging for toggle actions to capture detailed debug information and errors
    # TODO: Add comprehensive error handling to provide informative messages to users
    # TODO: Implement caching for toggle configurations to improve performance
    # TODO: Develop a simplified interface for common use cases to make configuration easier for users

    return mark_safe(js_code)
