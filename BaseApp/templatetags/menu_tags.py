from django import template

from BaseApp.menus import navbar_items

from BaseApp.utils import get_module_logger

logger = get_module_logger("menu_tags", __file__)

register = template.Library()


@register.inclusion_tag('BaseApp/ui_elements/nav_dropdown_buttons.html')
def top_navbar_buttons():
    """
    Returns a dictionary of nav items
    """
    logger.debug(f"navbar_items: {navbar_items}")
    return {'navbar_items': navbar_items}
