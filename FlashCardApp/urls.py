from django.urls import path
from . import views

urlpatterns = [
    path("", views.FlashCardAppView.as_view(), name="base"),
    path("decks/", views.FlashCardAppView.deck_list, name="deck_list"),
    path("decks/<int:deck_id>/",
         views.FlashCardAppView.deck_detail, name="deck_detail"),
]
