from typing import Any

from django.views.generic.base import TemplateView
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.urls import reverse

from BaseApp.utils import get_module_logger, require_htmx

module_logger = get_module_logger("views", __file__)


class BasePage(TemplateView):
    template_name = 'BaseApp/base.html'
    title = "Base"
    page_description = "This is a base template for all pages."
    page_disclaimer = ""
    header_is_extended = False

    def get_context_data(self, **kwargs: Any) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['page_description'] = self.page_description
        context['page_disclaimer'] = self.page_disclaimer
        context['header_is_extended'] = self.header_is_extended
        return context


class HomeView(BasePage):
    template_name = 'BaseApp/home/home.html'
    title = "Home"
    page_description = "I am a hobby developer who loves to learn and tinker with new technologies."
    page_disclaimer = "This website is a personal project to learn more about web development and to share my knowledge with others."
    header_is_extended = True


def get_django_info(request):
    template = loader.get_template('BaseApp/home/partials/django_info.html')
    context = {
        'django_version': "???",
    }
    return HttpResponse(template.render(context, request))


def get_tailwind_info(request):
    module_logger.debug("get_tailwind_info")
    template = loader.get_template(
        'BaseApp/home/partials/tailwind_partial.html')
    context = {
        'tailwind_version': "?",
    }
    return HttpResponse(template.render(context, request))


def get_htmx_info(request):
    template = loader.get_template(
        'BaseApp/home/partials/htmx_info.html')
    context = {
        'htmx_version': "??",
    }
    return HttpResponse(template.render(context, request))


class UIElementView(BasePage):
    template_name = 'BaseApp/ui_elements/base.html'
    title = "User Interface Elements"
    page_description = ""
    header_is_extended = True

    @require_htmx
    @staticmethod
    def get_buttons_examples(request):
        template = loader.get_template(
            'BaseApp/ui_elements/sections/buttons_examples.html')
        context = {
        }
        return HttpResponse(template.render(context, request))

    @require_htmx
    @staticmethod
    def get_toggled_content_examples(request):
        template = loader.get_template(
            'BaseApp/ui_elements/sections/toggled_content_examples.html')
        context = {
        }
        return HttpResponse(template.render(context, request))

    @require_htmx
    @staticmethod
    def get_button_example_minimal(request):
        template = loader.get_template(
            'BaseApp/ui_elements/partials/buttons/button_example_minimal.html')
        context = {
        }
        return HttpResponse(template.render(context, request))

    @require_htmx
    @staticmethod
    def content_toggle_basic(request):
        template = loader.get_template(
            'BaseApp/ui_elements/partials/content_toggle/basic.html')
        context = {
        }
        return HttpResponse(template.render(context, request))

    @require_htmx
    @staticmethod
    def content_toggle_multi_toggle_panel(request):
        template = loader.get_template(
            'BaseApp/ui_elements/partials/content_toggle/multi_toggle_panel.html')
        context = {
        }
        return HttpResponse(template.render(context, request))

    @require_htmx
    @staticmethod
    def content_toggle_forloop_accordian(request):
        template = loader.get_template(
            'BaseApp/ui_elements/partials/content_toggle/forloop_accordian.html')
        context = {
        }
        return HttpResponse(template.render(context, request))

    @require_htmx
    @staticmethod
    def content_toggle_hover_dropdown(request):
        template = loader.get_template(
            'BaseApp/ui_elements/partials/content_toggle/hover_dropdown.html')
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


@require_htmx
def get_back_button(request, url, target_element='none'):
    """
    Returns a back button for the given URL
    """
    if target_element == 'none':
        target_element = ''
    template = loader.get_template('BaseApp/navigation/back_button.html')
    context = {
        'previous_url': reverse(url),
        'back_button_target_element': target_element
    }
    return HttpResponse(template.render(context, request))
