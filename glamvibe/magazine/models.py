from django.db import models
from django.utils.text import slugify


class Post(models.Model):

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

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