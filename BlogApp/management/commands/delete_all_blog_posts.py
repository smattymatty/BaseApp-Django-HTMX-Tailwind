from django.core.management.base import BaseCommand
from BlogApp.models import BlogPost


class Command(BaseCommand):
    help = 'Deletes all blog posts'

    def handle(self, *args, **options):
        confirmation = input(
            "Are you sure you want to delete ALL blog posts? Type 'y' to confirm: ")
        if confirmation.lower() == 'y':
            blog_posts = BlogPost.objects.all()
            delete_count = blog_posts.delete()
            self.stdout.write(self.style.SUCCESS(
                f'Successfully deleted {delete_count[0]} blog posts'))
        else:
            self.stdout.write(self.style.WARNING('Deletion cancelled'))
