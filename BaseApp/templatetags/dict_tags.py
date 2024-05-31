from django import template

register = template.Library()


@register.filter(name='get_item')
def get_item(dictionary: dict, key):
    try:
        return dictionary[key]
    except KeyError:
        return None
    except Exception as e:
        return "Error: " + str(e)
