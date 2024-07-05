from django.shortcuts import render, get_object_or_404
from BaseApp.views import BasePage
from BaseApp.utils import require_htmx
from .models import Deck, Card


class FlashCardAppView(BasePage):
    template_name = "FlashCardApp/base.html"
    title = "Flash Card App"
    page_description = ""
    header_is_extended = True

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

    @staticmethod
    @require_htmx
    def card_answer_result(request, card_id):
        if request.method == 'POST':
            card = get_object_or_404(Card, pk=card_id)
            user_answer = request.POST.get('answer')
            correct_answer = card.question.answer

            context = {
                'card': card,
                'user_answer': user_answer,
                'correct_answer': correct_answer,
            }

            if not user_answer:
                context['result'] = 'Please enter an answer!'
                return render(request, 'FlashCardApp/sections/parts/card_answer_result.html', context)

            if card.question.type == "NUMERIC":
                try:
                    user_answer = float(user_answer)
                    correct_answer = float(correct_answer)
                    tolerance = 0.01  # Allow for small floating-point discrepancies
                    if abs(user_answer - correct_answer) < tolerance:
                        context['result'] = 'Correct!'
                    else:
                        context['result'] = f'Incorrect. The correct answer is {correct_answer}.'
                except ValueError:
                    context['result'] = 'Invalid input. Please enter a number.'

            elif card.question.type == "FREE_TEXT":
                # Case-insensitive comparison
                if user_answer.lower().strip() == correct_answer.lower().strip():
                    context['result'] = 'Correct!'
                else:
                    context['result'] = f'Incorrect. The correct answer is "{correct_answer}".'

            else:  # TRUE_FALSE or other types
                if user_answer == correct_answer:
                    context['result'] = 'Correct!'
                else:
                    context['result'] = f'Incorrect. The correct answer is {correct_answer}.'

            return render(request, 'FlashCardApp/sections/parts/card_answer_result.html', context)
