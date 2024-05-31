from django.shortcuts import render

from BaseApp.views import BaseView


class HtmxTodoView(BaseView):
    template_name = "HtmxApp/htmx_todo.html"
    title = "HTMX Todo App"
