from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__reload__/', include('django_browser_reload.urls')),
    path('', include(('BaseApp.urls', 'BaseApp'), namespace='BaseApp')),
    path('blog/', include(('BlogApp.urls', 'BlogApp'), namespace='BlogApp')),
    path('flash-card/', include(('FlashCardApp.urls',
         'FlashCardApp'), namespace='FlashCardApp')),
    path('accounts/', include('allauth.urls')),
    path('users/', include('UsersApp.urls')),
]
