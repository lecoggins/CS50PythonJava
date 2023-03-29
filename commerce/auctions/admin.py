from django.contrib import admin
from .models import AuctionListing, Category, Bid, Comment
# Register your models here.

admin.site.register(AuctionListing)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Comment)
