from django.urls import path
from .views import (
    BasePage, HomeView, UIElementView, ComponentsView, DocumentationView,
    ButtonsView, CardsView, TypographyView, get_django_info, get_tailwind_info,
    get_htmx_info, display_number
)

urlpatterns = [
    path('', BasePage.as_view(), name='base'),
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
         UIElementView.get_buttons_examples, name="buttons-examples"),
    path('ui-elements/menus/examples/',
         UIElementView.get_toggled_content_examples, name="toggled-content-examples"),
    path('display_number/', display_number, name="display_number"),
    path('ui-elements/buttons/examples/minimal/',
         UIElementView.get_button_example_minimal, name="button-example-minimal"),
    path('ui-elements/content-toggle/basic/',
         UIElementView.content_toggle_basic, name="content-toggle-basic"),
    path('ui-elements/content-toggle/multi-toggle-panel/',
         UIElementView.content_toggle_multi_toggle_panel, name="content-toggle-multi-toggle-panel"),
    path('ui-elements/content-toggle/forloop-accordian/',
         UIElementView.content_toggle_forloop_accordian, name="content-toggle-forloop-accordian"),
    path('ui-elements/content-toggle/hover-dropdown/',
         UIElementView.content_toggle_hover_dropdown, name="content-toggle-hover-dropdown"),
]
