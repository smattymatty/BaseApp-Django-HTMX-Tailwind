from django.shortcuts import render, get_object_or_404
from BaseApp.views import BasePage
from BaseApp.utils import require_htmx
from .models import Deck


class FlashCardAppView(BasePage):
    template_name = "FlashCardApp/base.html"
    title = "Flash Card App"
    page_description = "This is a flash card app."

    @staticmethod
    @require_htmx
    def deck_list(request):
        context = {
            'decks': Deck.objects.all(),
            'title': 'Deck List'  # Add a title for this view
        }
        return render(request, 'FlashCardApp/sections/deck_list.html', context)

    @staticmethod
    @require_htmx
    def deck_list_options(request):
        context = {}
        return render(request, 'FlashCardApp/sections/parts/options_menu/deck_list_options.html', context)

    @staticmethod
    @require_htmx
    def deck_detail(request, deck_id):
        deck = get_object_or_404(Deck, pk=deck_id)
        context = {
            'deck': deck,
            'title': f'Deck: {deck.name}'  # Dynamic title for each deck
        }
        return render(request, 'FlashCardApp/sections/deck_detail.html', context)

    @staticmethod
    @require_htmx
    def deck_detail_options(request, deck_id):
        deck = get_object_or_404(Deck, pk=deck_id)
        context = {
            'deck': deck,
        }
        return render(request, 'FlashCardApp/sections/parts/options_menu/deck_detail_options.html', context)
