from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return f"{self.id}: {self.categoryName}"

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=400) 
    price = models.FloatField()
    image_URL = models.CharField(max_length=1000, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="category")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user")
    isActive = models.BooleanField(null=False, blank=False)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="userWatchlist")

    def __str__(self):
        return f"{ self.id}: {self.title}"
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="commentUser")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, null=True, blank=True, related_name="commentListing")
    message = models.CharField(max_length=400) 
    dateTime = models.DateField()

    def __str__(self):
        return f"{self.author}: {self.message}"