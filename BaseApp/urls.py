from django.urls import path
from .views import BaseView, HomeView, UIElementView, ComponentsView, DocumentationView, ButtonsView, CardsView, TypographyView, get_django_info, get_tailwind_info, get_htmx_info, get_buttons_examples, get_menu_examples, display_number

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('home/', HomeView.as_view(), name="home"),
    path('ui-elements/', UIElementView.as_view(), name="ui-elements"),
    path('ui-elements/buttons/', ButtonsView.as_view(), name="buttons"),
    path('ui-elements/cards/', CardsView.as_view(), name="cards"),
    path('ui-elements/typography/', TypographyView.as_view(), name="typography"),
    path('components/', ComponentsView.as_view(), name="components"),
    path('documentation/', DocumentationView.as_view(), name="documentation"),
    # # H T M X - AJAX REQUESTS # #
    path('django-info/', get_django_info, name="django-info"),
    path('tailwind-info/', get_tailwind_info, name="tailwind-info"),
    path('htmx-info/', get_htmx_info, name="htmx-info"),
    path('ui-elements/buttons/examples/',
         get_buttons_examples, name="buttons-examples"),
    path('ui-elements/menus/examples/',
         get_menu_examples, name="menus-examples"),
    path('display_number/', display_number, name="display_number"),
]
