from django.urls import path

from .views import HtmxTodoView

urlpatterns = [
    path('todo/', HtmxTodoView.as_view(), name="htmx_todo"),
]
