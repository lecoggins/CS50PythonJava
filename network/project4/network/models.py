from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.CharField(max_length=1000, blank=True)

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_posts")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{ self.id}: {self.body}"
    