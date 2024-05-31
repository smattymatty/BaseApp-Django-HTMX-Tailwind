from django.db import models

from .models import BlogPost


def search_blog_posts(search_query, title=True, intro=True, author=True, content=False):
    """
    Search blog posts by specified fields.
    """
    query = models.Q()

    if title:
        query |= models.Q(title__icontains=search_query)
    if intro:
        query |= models.Q(intro__icontains=search_query)
    if author:
        query |= models.Q(author__username__icontains=search_query)
    if content:
        query |= models.Q(content__icontains=search_query)

    return BlogPost.objects.filter(query)
