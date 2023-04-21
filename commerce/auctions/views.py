from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User
from .models import Category
from .models import AuctionListing
from .models import Comment
from .models import Bid


def index(request):
    activeListing = AuctionListing.objects.filter(isActive=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html",{
        "active_listings": activeListing,
        "categories": categories
    })

def category_listings(request):
    if request.method == "POST":
        if request.POST['category'] == "all":
            return HttpResponseRedirect(reverse("index"))
        else:
            category = Category.objects.get(categoryName=request.POST['category'])
            activeListing = AuctionListing.objects.filter(isActive=True, category=category)
            categories = Category.objects.all()
            return render(request, "auctions/index.html",{
                "active_listings": activeListing,
                "categories": categories
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
        categoryData = Category.objects.get(categoryName=category)
        # get user information
        currentUser = request.user
        # new bid
        newBid = Bid(
            bid = starting_price,
            bidder = currentUser
        )

        newBid.save()

        # create a new listing
        newListing = AuctionListing(
            title = title,
            description = description,
            price = newBid,
            image_URL = imageURL,
            category = categoryData,
            owner = currentUser,
            isActive = True
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
    currentUser = request.user
    inWatchlist = currentUser in listingData.watchlist.all()
    comments = Comment.objects.filter(listing=listingData)
    highestBidder = listingData.price.bidder
    return render(request, "auctions/listing.html",{
        "listingData": listingData,
        "inWatchlist": inWatchlist,
        "currentUser": currentUser,
        "comments": comments,
        "highestBidder": highestBidder,
    })

def add_watchlist(request, listing_id):
    currentUser = request.user
    listingData = AuctionListing.objects.get(id=listing_id)
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))    

def remove_watchlist(request, listing_id):
    currentUser = request.user
    listingData = AuctionListing.objects.get(id=listing_id)
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))

def watchlist(request):
    currentUser = request.user
    watchlistListings= AuctionListing.objects.filter(watchlist=currentUser)
    categories = Category.objects.all()
    return render(request, "auctions/watchlist.html",{
        "watchlistListings": watchlistListings,
        "categories": categories,
    })

def watchlist_category_listings(request):
    if request.method == "POST":
        if request.POST['category'] == "all":
            return HttpResponseRedirect(reverse("watchlist"))
        else:
            category = Category.objects.get(categoryName=request.POST['category'])
            currentUser = request.user
            watchlistListings= AuctionListing.objects.filter(watchlist=currentUser, category=category)
            categories = Category.objects.all()
            return render(request, "auctions/watchlist.html",{
                "watchlistListings": watchlistListings,
                "categories": categories,
            })
        
def comment(request, listing_id):
    if request.method == "POST":
        author = request.user
        listing = AuctionListing.objects.get(pk=listing_id)
        message = request.POST['comment']
        dateTime = datetime.now()
    
        # create a new comment
        newComment = Comment(
            author = author,
            listing = listing,
            message = message,
            dateTime = dateTime
        )
        # save new comment
        newComment.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id, )))
    
def bid(request, listing_id):
    if request.method == "POST":
        listingData = AuctionListing.objects.get(id=listing_id)
        currentUser = request.user
        inWatchlist = currentUser in listingData.watchlist.all()
        comments = Comment.objects.filter(listing=listingData)
        newBid = float(request.POST['bid'])
        currentPrice = float(listingData.price.bid)
        danger = "danger"
        if (newBid <= currentPrice):
            message = "Bid must be greater than the current price"
            return render(request, "auctions/listing.html",{
                "listingData": listingData,
                "inWatchlist": inWatchlist,
                "currentUser": currentUser,
                "comments": comments,
                "message": message,
                "type": danger
            })
        else:
            enterBid = Bid(
                bid = newBid,
                bidder = currentUser
            )
            enterBid.save()

            listingData.price = enterBid
            listingData.numberOfBids = listingData.numberOfBids + 1
            listingData.save()

            message = "Bid successful"
            success = "success"
            return render(request, "auctions/listing.html",{
                "listingData": listingData,
                "inWatchlist": inWatchlist,
                "currentUser": currentUser,
                "comments": comments,
                "message": message,
                "type": success
            })

def close_listing(request, listing_id):
    if request.method=="POST":
        listingData = AuctionListing.objects.get(id=listing_id)
        listingData.isActive = "False"
        listingData.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id, )))
