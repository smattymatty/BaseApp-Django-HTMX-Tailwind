from django.urls import path
from . import views

urlpatterns = [
    path("", views.FlashCardAppView.as_view(), name="base"),
    path("decks/", views.FlashCardAppView.deck_list, name="deck_list"),
]
