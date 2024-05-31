from django.urls import reverse

from .styles import BasicButtonStyle, DerangedButtonStyle, DerangedDropdownStyle, BasicDropdownStyle


class DropdownNavItem:
    """
    NavItem class representing a single nav item in the nav dropdown
    """

    def __init__(self, name, url,
                 button_style=BasicButtonStyle,
                 dropdown_style=BasicDropdownStyle,):
        self.name = name
        self.url = url
        self.button_style: str = button_style.classes
        self.dropdown_style: str = dropdown_style.classes

    def __str__(self):
        return f"{self.name} ({self.url})"

    def __repr__(self):
        return self.__str__()


navbar_items = {
    "Documentation": [
        DropdownNavItem("Blog", reverse('BlogApp:blog')),
        DropdownNavItem("Home", reverse('BaseApp:home')),
        DropdownNavItem("Home", reverse('BaseApp:home')),
    ],
    "Components": [
        DropdownNavItem("User Interface", reverse('BaseApp:ui-elements')),
        DropdownNavItem("Home", reverse('BaseApp:home')),
    ],
    "Tools": [
        DropdownNavItem("Home", reverse('BaseApp:home')),
    ],
}
