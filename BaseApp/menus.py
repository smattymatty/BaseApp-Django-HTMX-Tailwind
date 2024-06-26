from django.urls import reverse


class DropdownNavItem:
    """
    NavItem class representing a single nav item in the nav dropdown
    """

    def __init__(self, name, url):
        self.name = name
        self.url = url

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
        DropdownNavItem("Flash Cards", reverse('FlashCardApp:base')),
    ],
}
