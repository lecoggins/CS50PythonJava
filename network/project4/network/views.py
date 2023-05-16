from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.http import JsonResponse

from .models import User, Post, Follower, Like

def like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = user.objects.get(pk=request.user.id)
    newlike = Like(user=user, post=post)
    newlike.save()
    return JsonResponse({"message": "Like added"})

    
def unlike(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = user.objects.get(pk=request.user.id)
    like = Like.objects.filter(user=user, post=post)
    like.delete()
    post=()
    return JsonResponse({"message": "Like removed"})

def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        edit_post = Post.objects.get(pk=post_id)
        edit_post.body = data["content"]
        edit_post.save()
        return JsonResponse({"message": "Change Successful", "data": data["content"]})


def index(request):
    if request.method == "POST":
        
        currentUser = request.user
        postBody = request.POST['body']
        dateTime = datetime.now()

        newPost = Post(
            user = currentUser,
            body = postBody,
            timestamp = dateTime
        )
        newPost.save()

        posts = Post.objects.all().order_by("id").reverse()
        return HttpResponseRedirect(reverse("index"))
    
    else:
        posts = Post.objects.all().order_by("id").reverse()
        paginated = Paginator(posts, 10)
        pageNumber = request.GET.get('page')
        pagePosts = paginated.get_page(pageNumber)
        likes = Like.objects.all()

        userLikes = []
        try:
            for like in likes:
                if like.user.id == request.user.id:
                    userLikes.append(like.post.id)
        except:
            userLikes = []

        return render(request, "network/index.html", {
            "posts": pagePosts,
            "userLikes": userLikes
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

    
def profile(request, user_id):
    requestedUser = User.objects.get(id=user_id)
    posts = Post.objects.filter(user=requestedUser).order_by("id").reverse()
    currentUser = request.user
    followers = Follower.objects.filter(user=requestedUser)
    isFollowing = "False"
    isCurrent = "False"
    for follower in followers:
        if follower.follower == currentUser:
            isFollowing = "True"
    if currentUser == requestedUser:
        isCurrent = "True"
    noFollowers = len(followers)
    noPosts = len(Post.objects.filter(user=requestedUser))
    noFollowing = len(Follower.objects.filter(follower=requestedUser))

    paginated = Paginator(posts, 10)
    pageNumber = request.GET.get('page')
    pagePosts = paginated.get_page(pageNumber)

    return render(request, "network/profile.html",{
        "posts": pagePosts,
        "userName": requestedUser.username,
        "currentUser": currentUser,
        "noFollowers": noFollowers,
        "noPosts": noPosts,
        "noFollowing": noFollowing,
        "followers": followers,
        "isFollowing": isFollowing,
        "isCurrent": isCurrent,
        "requestedUser": requestedUser
    })

def follow(request):
    if request.method=="POST":
        currentUser = request.user
        otheruser = request.POST['userToFollow']
        userFollow = User.objects.get(username=otheruser)
        user_id = userFollow.id

        newFollow = Follower(
            user = userFollow,
            follower = currentUser
        )
        newFollow.save()
        return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))



def unfollow(request):
    if request.method=="POST":
        currentUser = request.user
        otheruser = request.POST['userToUnfollow']
        userFollow = User.objects.get(username=otheruser)
        user_id = userFollow.id

        unfollow = Follower.objects.get(user = userFollow, follower = currentUser)
        unfollow.delete()
        return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))

def following(request):
    currentUser = request.user
    allFollowing = Follower.objects.filter(follower = currentUser)
    following = []
    for each in allFollowing:
        follow = each.user
        following.append(follow)
    posts = []
    allPosts = Post.objects.all().order_by("id").reverse()
    for post in allPosts:
        if post.user in following:
            posts.append(post)

    paginated = Paginator(posts, 10)
    pageNumber = request.GET.get('page')
    pagePosts = paginated.get_page(pageNumber)

    return render(request, "network/following.html",{
        "posts": pagePosts,
        "following": following
    })