from django import template

register = template.Library()

@register.filter
def concat(value, arg):
    """Concatenates the given argument to the value"""
    return str(value) + str(arg)