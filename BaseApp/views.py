from typing import Any

from django.views.generic.base import TemplateView
from django.template import loader
from django.http import HttpResponse

from BaseApp.utils import get_module_logger

module_logger = get_module_logger("views", __file__)


class BaseView(TemplateView):
    template_name = 'BaseApp/base.html'
    title = "Base"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class HomeView(BaseView):
    template_name = 'BaseApp/home/home.html'
    title = "Home"


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


class UIElementView(BaseView):
    template_name = 'BaseApp/ui_elements/ui-elements.html'
    title = "UI Elements"


def get_buttons_examples(request):
    template = loader.get_template(
        'BaseApp/ui_elements/sections/buttons_examples.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


class ComponentsView(BaseView):
    template_name = 'BaseApp/components.html'
    title = "Components"


class DocumentationView(BaseView):
    template_name = 'BaseApp/documentation.html'
    title = "Documentation"


class ButtonsView(BaseView):
    template_name = "BaseApp/ui_elements/buttons.html"
    title = "UI Elements - Buttons"


class CardsView(BaseView):
    template_name = "BaseApp/ui_elements/cards.html"
    title = "UI Elements - Cards"


class TypographyView(BaseView):
    template_name = "BaseApp/ui_elements/typography.html"
    title = "UI Elements - Typography"
