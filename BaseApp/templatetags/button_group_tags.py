import re

from django import template
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from BaseApp.exceptions import TemplateTagInitError
from BaseApp.utils import get_module_logger

module_logger = get_module_logger("templatetags", __file__)

register = template.Library()

VALID_GROUP_ID_PATTERN = re.compile(r'^[a-zA-Z0-9_\-]+$')


@register.simple_tag(takes_context=True)
def init_toggled_button_groups(context, *group_ids: str):
    """
    Generates the JavaScript code to initialize ToggledButtonGroup instances.
    Args:
        *group_ids: Variable number of button group IDs.
    Returns:
        Safe JavaScript code string.
    """
    group_ids = [group_id.strip() for group_id in group_ids]
    reserved_suffix = "-toggled-button-group"
    if not group_ids:
        raise TemplateTagInitError(
            "init_toggled_button_groups tag requires at least one button group ID.", reserved_suffix
        )
    for group_id in group_ids:
        if reserved_suffix in group_id:
            raise TemplateTagInitError(
                f"Invalid group ID '{group_id}'.", reserved_suffix
            )
        if not VALID_GROUP_ID_PATTERN.match(group_id):
            raise TemplateTagInitError(
                f"Group ID '{group_id}' contains invalid characters. Only alphanumeric characters, hyphens, and underscores are allowed.", reserved_suffix
            )
    context['TOGGLED_BUTTON_GROUPS_INITIALIZED'] = True

    module_path = static("BaseApp/modules/ToggledButtonGroup.mjs")
    js_code = f"""
        <script type="module">
            import {{ ToggledButtonGroup }} from "{module_path}";
            ToggledButtonGroup.initAll('{ " ".join(group_ids) }');
        </script>
    """
    return mark_safe(js_code)
