from django.shortcuts import render
from BaseApp.views import BasePage
from BaseApp.utils import require_htmx
from .models import Deck


class FlashCardAppView(BasePage):
    """
    The main view for the FlashCardApp
    This is a container for all of it's staticmethod views
    Usage in urls.py:
        path('', FlashCardAppView.as_view(), name="base"),
        path('decks/', FlashCardAppView.deck_list, name="deck_list"),
    """
    template_name = "FlashCardApp/base.html"
    title = "Flash Card App"
    page_description = "This is a flash card app."

    @staticmethod
    @require_htmx
    def deck_list(request):
        """
        This view is used to display a list of all decks in the database
        """
        context = {
            'decks': Deck.objects.all()
        }
        return render(
            request,
            'FlashCardApp/sections/deck_list.html',
            context
        )
