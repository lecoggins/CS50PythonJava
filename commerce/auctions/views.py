from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User
from .models import Category
from .models import AuctionListing


def index(request):
    return render(request, "auctions/index.html",{
        "active_listings": AuctionListing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == "POST":
        # get information about new lsiting
        title = request.POST["listing_title"]
        description = request.POST["listing_description"]
        starting_price = float(request.POST["starting_price"])
        imageURL = request.POST["image_url"]
        category = request.POST["category"]
        #get all information about category to allow refernce to category table
        categoryData = Category.objects.get(category=category)
        # get user information
        currentUser = request.user
        # create a new listing
        newListing = AuctionListing(
            title = title,
            description = description,
            starting_bid = starting_price,
            image_URL = imageURL,
            category = categoryData,
            owner = currentUser
        )
        # save new listing
        newListing.save()
        # redirect to index
        return HttpResponseRedirect(reverse("index"))

    # if get - render create listing html
    else:
        return render(request, "auctions/create.html",{
            "categories": Category.objects.all()
        })
    
def listing(request, listing_id):
        listingData = AuctionListing.objects.get(id=listing_id)
        return render(request, "auctions/listing.html",{
            "listingData": listingData
        })