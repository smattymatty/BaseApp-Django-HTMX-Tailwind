from django import template
from django.templatetags.static import static
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def init_button_groups(*group_ids):
    """
    Generates the JavaScript code to initialize ToggledButtonGroup instances.

    Args:
        *group_ids: Variable number of button group IDs.

    Returns:
        Safe JavaScript code string.
    """

    if not group_ids:
        return ""

    module_path = static("BaseApp/modules/ToggledButtonGroup.mjs")

    js_code = f"""
        <script type="module">
            import {{ ToggledButtonGroup }} from "{module_path}";
            ToggledButtonGroup.initAll('{ " ".join(group_ids) }');
        </script>
    """

    return mark_safe(js_code)
