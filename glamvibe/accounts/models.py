from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username