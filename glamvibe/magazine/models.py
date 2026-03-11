from django.db import models
from django.utils.text import slugify


class Category(models.Model):

    name = models.CharField(max_length=50)

    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    content = models.TextField()

    image = models.ImageField(upload_to="magazine/")

    views = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        if not self.slug and self.title:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/magazine/{self.slug}/"

