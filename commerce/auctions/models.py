from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return f"{self.id}: {self.category}"

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.FloatField()
    image_URL = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="Listings")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user")

    def __str__(self):
        return f"{ self.id}: {self.title}"

class Bid(models.Model):
    pass

class Comment(models.Model):
    pass