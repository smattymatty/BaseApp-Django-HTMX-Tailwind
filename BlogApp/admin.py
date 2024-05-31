from django.contrib import admin
from .models import BlogCategory, BlogPost


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author',
                    'created_at', 'updated_at', 'color')
    list_filter = ('category', 'author', 'created_at')
    # Search by author's username as well
    search_fields = ('title', 'content', 'author__username')
    date_hierarchy = 'created_at'  # Add a date-based drilldown navigation
    # Automatically generate slug from title
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        # Optimize queryset for list display
        qs = super().get_queryset(request)
        return qs.select_related('author', 'category')
