from typing import Any

from django.views.generic.base import TemplateView
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.http import require_POST

from BaseApp.utils import get_module_logger

module_logger = get_module_logger("views", __file__)


class BasePage(TemplateView):
    template_name = 'BaseApp/base.html'
    title = "Base"
    page_description = "This is a base template for all pages."
    page_disclaimer = ""
    extended_header = False

    def get_context_data(self, **kwargs: Any) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['page_description'] = self.page_description
        context['page_disclaimer'] = self.page_disclaimer
        context['extended_header'] = self.extended_header
        return context


class HomeView(BasePage):
    template_name = 'BaseApp/home/home.html'
    title = "Home"
    page_description = "I am a hobby developer who loves to learn and tinker with new technologies."
    page_disclaimer = "This website is a personal project to learn more about web development and to share my knowledge with others."
    extended_header = True


def get_django_info(request):
    template = loader.get_template('BaseApp/home/partials/django_info.html')
    context = {
        'django_version': "5.0.2",
    }
    return HttpResponse(template.render(context, request))


def get_tailwind_info(request):
    module_logger.debug("get_tailwind_info")
    template = loader.get_template(
        'BaseApp/home/partials/tailwind_partial.html')
    context = {
        'tailwind_version': "3.0.24",
    }
    return HttpResponse(template.render(context, request))


def get_htmx_info(request):
    template = loader.get_template(
        'BaseApp/home/partials/htmx_info.html')
    context = {
        'htmx_version': "3.0.4",
    }
    return HttpResponse(template.render(context, request))


class UIElementView(BasePage):
    template_name = 'BaseApp/ui_elements/base.html'
    title = "User Interface Elements"
    page_description = ""
    extended_header = True


def get_buttons_examples(request):
    template = loader.get_template(
        'BaseApp/ui_elements/sections/buttons_examples.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def get_menu_examples(request):
    template = loader.get_template(
        'BaseApp/ui_elements/sections/menu_examples.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def get_button_example_minimal(request):
    template = loader.get_template(
        'BaseApp/ui_elements/partials/buttons/button_example_minimal.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


class ComponentsView(BasePage):
    template_name = 'BaseApp/components.html'
    title = "Components"


class DocumentationView(BasePage):
    template_name = 'BaseApp/documentation.html'
    title = "Documentation"


class ButtonsView(BasePage):
    template_name = "BaseApp/ui_elements/buttons.html"
    title = "UI Elements - Buttons"


class CardsView(BasePage):
    template_name = "BaseApp/ui_elements/cards.html"
    title = "UI Elements - Cards"


class TypographyView(BasePage):
    template_name = "BaseApp/ui_elements/typography.html"
    title = "UI Elements - Typography"


@require_POST
def display_number(request):
    try:
        # Retrieve the button value from the POST daa
        number = request.POST.get('number')
        # Log the received number (for debugging)
        module_logger.info(f"Received number: {number}")

        # Render the template with the number
        template = loader.get_template('BaseApp/tests/number_display.html')
        context = {'number': number}
        return HttpResponse(template.render(context, request))

    except Exception as e:
        # Handle exceptions and log errors
        module_logger.error(f"Error in display_number: {e}")
        if settings.DEBUG:
            return JsonResponse({'error': f'Error: {e}'}, status=500)
        else:
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
