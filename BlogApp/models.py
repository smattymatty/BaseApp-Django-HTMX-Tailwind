from django.db import models

from BaseApp.constants import COLORS


class BlogCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class BlogPost(models.Model):
    author = models.ForeignKey('UsersApp.User', on_delete=models.CASCADE)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    title = models.CharField(max_length=64)
    intro = models.CharField(max_length=128, blank=True, null=True)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # for styling
    color = models.CharField(
        max_length=6, default=COLORS[0],
        choices=zip(COLORS, COLORS)
    )
    title_length = models.IntegerField(default=0)  # controls font size
    intro_length = models.IntegerField(default=0)  # controls font size

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        self.title_length = len(self.title)
        self.intro_length = len(self.intro)
        super().save(*args, **kwargs)
