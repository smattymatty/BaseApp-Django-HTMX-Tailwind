from django import template

from BaseApp.menus import navbar_items

from BaseApp.utils import get_module_logger

logger = get_module_logger("menu_tags", __file__)

register = template.Library()


@register.inclusion_tag('BaseApp/navigation/nav_dropdown_buttons.html')
def top_navbar_buttons():
    """
    Returns a dictionary of nav items
    """
    logger.debug(f"navbar_items: {navbar_items}")
    return {'navbar_items': navbar_items}


@register.inclusion_tag('BaseApp/navigation/back_button.html', takes_context=True)
def back_button(context, target_element):
    previous_url = context['previous_url']
    return {
        'previous_url': previous_url,
        'back_button_target_element': target_element
    }
