from django.urls import path

from .views import BlogView, get_blog_post_list

urlpatterns = [
    path('', BlogView.as_view(), name="blog"),
    # #
    path('blog-post-list/', get_blog_post_list, name="blog-post-list"),
]
