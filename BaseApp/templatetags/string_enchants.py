from django import template

register = template.Library()

@register.filter
def concat(value, arg):
    """Concatenates the given argument to the value"""
    return str(value) + str(arg)

@register.filter
def split(value, arg):
    """
    Splits the value by the argument and returns a list.
    Usage: {{ value|split:"," }}
    """
    return value.split(arg)

@register.filter
def replace(value, arg):
    """
    Replaces all occurrences of a string with another string.
    Usage: {{ value|replace:"old,new" }}
    """
    old, new = arg.split(',')
    return value.replace(old, new)