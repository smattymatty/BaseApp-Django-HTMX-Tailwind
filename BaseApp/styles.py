from .constants import background_colors, background_border_colors

registered_styles = {}


class TailwindStyle:
    """
    Tailwind style class. 
    Running python manage.py generate_tailwind_dummy will generate a 
    dummy HTML file for Tailwind CSS classes in the templates directory

    Attributes:
        classes (str): Tailwind style classes
    """
    classes: str = ""

    def __init__(self, classes: str):
        self.classes = classes


def register_style(name=None):
    """
    Decorator factory to register a style class with a custom name.
    This is to ensure python manage.py tailwind_dummy will 
    generate a dummy HTML file for Tailwind CSS classes in 
    the templates

    args:
        name (str, optional): Name of the style class. Defaults to class.__name__.
    """
    def decorator(style_class):
        class_name = name if name is not None else style_class.__name__
        registered_styles[class_name] = style_class
        return style_class
    return decorator


@register_style(name="basic-button")
class BasicButtonStyle(TailwindStyle):
    """
    Style class for the basic button style
    """
    classes = f"""
    transition-all duration-200 ease-linear text-white/50
    my-2 pt-1 border-x rounded-md 
    md:text-base text-sm
    {background_border_colors[1]}
    hover:{background_colors[2]} 
    {background_border_colors[1]}
    hover:{background_border_colors[0]}
    hover:text-white
    hover:font-bold
    hover:cursor-pointer
    hover:border-x-4 hover:rounded-lg hover:my-0 hover:pt-3
    """


@register_style(name="deranged-button")
class DerangedButtonStyle(TailwindStyle):
    """
    Button style for the utterly deranged
    """
    classes = f"""
    active
    transition-all duration-200 ease-linear text-black/50
    my-2 pt-1 border-x rounded-md 
    bg-red-500
    hover:bg-red-600
    border-red-800
    hover:{background_border_colors[0]}
    hover:text-black
    hover:font-bold
    hover:cursor-pointer
    hover:border-x-4 hover:rounded-lg hover:my-0 hover:pt-3
    """


@register_style(name="basic-dropdown")
class BasicDropdownStyle(TailwindStyle):
    """
    Basic dropdown style
    """
    classes = f"""
    font-normal
    transition-all duration-200 ease-linear text-white/50 shadow-md shadow-black
    absolute top-full left-0 w-full flex flex-col border-x-2 rounded-b-md
    {background_colors[2]} 
    {background_border_colors[0]}
    [&>a]:text-white/50
    hover:[&>a]:text-white
    hover:[&>a]:cursor-pointer
    [&>a]:{background_colors[1]}
    hover:[&>a]:{background_colors[2]} 
    shadow-md shadow-black
    """


@register_style(name="deranged-dropdown")
class DerangedDropdownStyle(TailwindStyle):
    """
    Dropdown style for the utterly deranged
    """
    classes = f"""
    font-normal
    transition-all duration-200 ease-linear text-white/50 shadow-md shadow-black
    absolute top-full left-0 w-full flex flex-col border-x-2 rounded-b-md
    bg-green-500
    boder-green-800
    [&>a]:text-black/50 [&>a]:py-1
    hover:[&>a]:text-black
    hover:[&>a]:cursor-pointer
    [&>a]:bg-green-500
    hover:[&>a]:bg-green-700
    shadow-md shadow-black
    """
