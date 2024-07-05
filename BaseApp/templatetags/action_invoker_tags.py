from django import template
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from BaseApp.exceptions import TemplateTagInitError
from BaseApp.utils import get_module_logger

module_logger = get_module_logger("templatetags", __file__)

register = template.Library()

# Allowed values for event and action
ALLOWED_EVENTS = {'on-load'}
ALLOWED_ACTIONS = {'click', 'toggle'}
VALID_STRATEGIES = [
    'all', 'first', 'last', 'none', 'random', 'byText'
]


@register.simple_tag
def invoke_action(event, action, strategy, target_id):
    """
    Generates the JavaScript code to initialize ActionInvoker instances.

    Args:
        event: The event to listen for (e.g., "on-load").
        action: The action to take (e.g., "click").
        strategy: The strategy to use for selecting buttons (e.g., "all").
        target_id: The ID of the element to attach the event listener to.

    Returns:
        Safe JavaScript code string.

    Raises:
        TemplateTagInitError: If validation fails.

    Example usage:
        {% load action_invoker_tags %}
        {% invoke_action "on-load" "click" "all" "my-button-group" %}
    """
    module_logger.debug(
        f"invoke_action tag generated JavaScript code: event: {event}, action: {action}, strategy: {strategy}, target_id: {target_id}")

    # TODO: Add further validation for the `event`, `action`, and `strategy` parameters as needed
    # TODO: Ensure that the `target_id` exists in the document before proceeding
    # TODO: Consider adding configuration settings to handle different types of events, actions, and strategies
    # TODO: Add support for adding custom attributes or options in the generated JavaScript code
    # TODO: Add support for dynamically binding events to newly added DOM elements
    # TODO: Load configurations based on the environment (e.g., different configurations for development, staging, production)
    # TODO: Allow users to define custom actions and events through the Django settings
    # TODO: Implement template inheritance for invoke_action configurations to allow sharing common configurations across templates
    # TODO: Add a debug mode to log detailed information about the initialization process and actions performed
    # TODO: Integrate performance monitoring to log the execution time of actions and event handlers
    # TODO: Add support for preserving the state of actions across page reloads (e.g., using localStorage or sessionStorage)
    # TODO: Ensure the generated JavaScript code is accessible and follows best practices (e.g., ARIA roles, keyboard navigation)
    # TODO: Add support for internationalization to handle different languages and locales
    # TODO: Implement enhanced logging for invoke_action to capture detailed debug information and errors
    # TODO: Add comprehensive error handling to provide informative messages to users
    # TODO: Implement caching for invoke_action configurations to improve performance
    # TODO: Develop a simplified interface for common use cases to make configuration easier for users

    # Validate parameters
    try:
        if not event or not action or not target_id:
            raise ValueError(
                "Missing required parameters: event, action, and target_id must be provided.")

        if event not in ALLOWED_EVENTS:
            raise ValueError(
                f"Invalid event: {event}. Allowed events are: {', '.join(ALLOWED_EVENTS)}.")
        if strategy not in VALID_STRATEGIES and not (strategy.isdigit() and 0 <= int(strategy) <= 100):
            raise ValueError(
                f"Invalid strategy: {strategy}. Allowed strategies are: {', '.join(VALID_STRATEGIES)} or an index between 0 and 100.")
        if action not in ALLOWED_ACTIONS:
            raise ValueError(
                f"Invalid action: {action}. Allowed actions are: {', '.join(ALLOWED_ACTIONS)}.")

        if not isinstance(target_id, str) or not target_id.strip():
            raise ValueError(
                "Invalid target_id: It must be a non-empty string.")
    except ValueError as e:
        # Log and raise a TemplateTagInitError with a helpful message
        module_logger.error(f"Validation error: {e}")
        raise TemplateTagInitError(str(e))

    module_path = static("BaseApp/modules/ActionInvoker.mjs")

    # Generate the JavaScript code
    js_code = f"""
        <script type="module">
            import {{ ActionInvoker }} from "{module_path}";
            ActionInvoker.initAll([{{ event: "{event}", action: "{action}", targetId: "{target_id}", strategy: "{strategy}" }}]);
        </script>
    """

    return mark_safe(js_code)
