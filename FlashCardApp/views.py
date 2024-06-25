from django.shortcuts import render, get_object_or_404

from BaseApp.views import BasePage
from BaseApp.utils import require_htmx

from .models import Deck


class FlashCardAppView(BasePage):
    """
    The main view for the FlashCardApp
    """
    template_name = "FlashCardApp/base.html"
    title = "Flash Card App"
    page_description = "This is a flash card app."

    @staticmethod
    @require_htmx
    def deck_list(request):
        """
        Display a list of all decks in the database
        """
        context = {
            'decks': Deck.objects.all()
        }
        return render(
            request,
            'FlashCardApp/sections/deck_list.html',
            context
        )

    @staticmethod
    @require_htmx
    def deck_detail(request, deck_id):
        """
        Display the details of a specific deck
        """
        context = {
            'deck': get_object_or_404(Deck, pk=deck_id)
        }
        return render(
            request,
            'FlashCardApp/sections/deck_detail.html',
            context
        )
