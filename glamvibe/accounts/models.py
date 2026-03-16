from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)

    bio = models.TextField(blank=True)

    followers = models.ManyToManyField(User, related_name="following", blank=True)

    def __str__(self):
        return self.user.username