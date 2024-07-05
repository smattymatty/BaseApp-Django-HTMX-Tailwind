from django.urls import path
from . import views

# Main App URLs
urlpatterns = [
    path("", views.FlashCardAppView.as_view(), name="base"),
    path("decks/", views.FlashCardAppView.deck_list, name="deck_list"),
    path("decks/<int:deck_id>/",
         views.FlashCardAppView.deck_detail, name="deck_detail"),
]

# Smaller URLS for each view
url_bits = [
    path("decks/<int:deck_id>/options/",
         views.FlashCardAppView.deck_detail_options, name="deck_options"),
    path("decks/options/",
         views.FlashCardAppView.deck_list_options, name="deck_list_options"),
    path("card/<int:card_id>/answer/",
         views.FlashCardAppView.card_answer_result, name="card_answer_result"),
]

urlpatterns += url_bits
