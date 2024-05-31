import time

from django.core.paginator import Paginator
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

import BlogApp.logic as logic
from BaseApp.views import BaseView
from BaseApp.utils import get_module_logger
from core import settings

from .models import BlogCategory, BlogPost

module_logger = get_module_logger("views", __file__)


class BlogView(BaseView):
    template_name = 'BlogApp/blog.html'
    title = "Blog"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog_categories'] = BlogCategory.objects.all()
        return context


@require_http_methods(['POST'])
def get_blog_post_list(request):
    page_size = 8
    try:
        # SETUP THE DATA
        page_number = int(request.POST.get('page', 1))  # Default to page 1
        search_query = request.POST.get('search_query', '')
        # lOG THE DATA
        module_logger.debug(f"{page_number=}, {search_query=}")
        # CHECK IF THERE IS A SEARCH QUERY
        if search_query:
            blog_posts = logic.search_blog_posts(search_query)
        else:
            blog_posts = BlogPost.objects.all()
        # SPLIT THE DATA INTO A PAGES
        paginator = Paginator(blog_posts, page_size)
        # 0 MEANS NO MORE PAGES
        if page_number == 0:  # empy response
            return HttpResponse('')
        # GET THE PAGE
        page_obj = paginator.get_page(page_number)
        # RENDER THE TEMPLATE
        template = loader.get_template('BlogApp/sections/blog_post_list.html')
        context = {
            'blog_posts': page_obj,
            'has_next': page_obj.has_next(),
        }
        return HttpResponse(template.render(context, request))
    except Exception as e:
        module_logger.error(e)
        print(f"Error in get_blog_post_list: {e}")
        if settings.DEBUG:
            return JsonResponse(
                {'error': f'Error in get_blog_post_list:\n {e}'},
                status=500)
        return JsonResponse(
            {'error': 'Internal Server Error'},
            status=500)
