from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.CharField(max_length=1000, blank=True, default="https://www.shutterstock.com/image-vector/default-avatar-profile-trendy-style-260nw-1759726295.jpg")
    posts = models.IntegerField(default=0)

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_posts")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField()
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{ self.id}: {self.body}"

class Follower(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_followed")
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="individual_follower")

    def __str__(self):
        return f"{ self.follower} is following {self.user}"
    
class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_likes")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_likes")

    def __str__(self):
        return f"{self.user} likes {self.post}"