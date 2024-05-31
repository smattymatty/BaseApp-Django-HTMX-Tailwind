# blog_app/management/commands/generate_blog_posts.py
import random

from faker import Faker
from django.core.management.base import BaseCommand


from BlogApp.models import BlogPost, BlogCategory
from UsersApp.models import User
from BaseApp.constants import COLORS


class Command(BaseCommand):
    help = 'Generates random blog posts'

    def add_arguments(self, parser):
        parser.add_argument('num_posts', type=int,
                            help='The number of blog posts to create')

    def handle(self, *args, **options):
        num_posts = options['num_posts']
        fake = Faker()

        # Get all available categories
        categories = list(BlogCategory.objects.all())
        if not categories:
            self.stdout.write(self.style.WARNING(
                'No categories found. Creating 5 Random Categories...'))
            categories = self.create_random_categories()

        # Get all available authors (users)
        authors = list(User.objects.all())
        if not authors:
            self.stdout.write(self.style.WARNING(
                'No authors found. Creating a Random Author...'))
            authors = [self.create_random_user(fake)]  # Create one random user

        for _ in range(num_posts):
            title = fake.sentence()[:64]  # Limit title to 64 characters
            intro = fake.paragraph()[:128]  # Limit intro to 128 characters
            content = fake.text()
            category = random.choice(categories)
            author = random.choice(authors)
            # Assuming you have COLORS defined as a list
            color = random.choice(COLORS)

            BlogPost.objects.create(
                title=title,
                intro=intro,
                content=content,
                category=category,
                author=author,
                color=color,
            )

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {num_posts} blog posts'))

    def create_random_categories(self, num_categories=5):
        """Creates random blog categories using Faker."""
        fake = Faker()
        categories = []

        for _ in range(num_categories):
            category_name = fake.unique.bs()  # Get a unique "bs" (business buzzword)
            category = BlogCategory.objects.create(
                name=category_name,
            )
            categories.append(category)

        return categories

    def create_random_user(self, fake):
        """Creates a random user using Faker."""

        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f"{first_name.lower()}_{last_name.lower()}"

        # Ensure username is unique
        while User.objects.filter(username=username).exists():
            username = f"{username}_{random.randint(1, 1000)}"

        email = fake.email()
        password = fake.password()

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        return user
