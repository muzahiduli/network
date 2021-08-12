from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, request
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json


from .models import User, Post, Follow

@csrf_exempt
def following(request, name):
    if request.method == "PUT":
        follower = request.user
        following = User.objects.get(username=name)
        data = json.loads(request.body)
        
        if (data.get('follow') == True):
            try: 
                follow = Follow.objects.get(follower=follower)
            except:
                follow = Follow(follower=follower)
                follow.save()
            
            follow.following.add(following)
            follow.save()
        else:
            follow = Follow.objects.get(follower=follower)
            follow.following.remove(following)
            follow.save()

        followers = Follow.objects.filter(following=following).count()
        return JsonResponse({"followers": followers}, status=201)

@csrf_exempt
def profile(request, name):
    try:
        profile = User.objects.get(username=name)
    except:
        return render(request, "network/index.html", {
            "invalid": True
        })

    posts = profile.posts.all().order_by('-timestamp')
    followers = Follow.objects.filter(following=profile).count()
    try:
        following = Follow.objects.get(follower=profile).following.count()
    except:
        following = 0
    
    #Check if current user is following or not following the profile user
    try:
        follow = Follow.objects.get(follower=request.user)
        if (profile in follow.following.all()):
            userFollowing = True
        else:
          userFollowing = False  
    except:
        userFollowing = False

    return render(request, "network/index.html", {
        "posts": posts,
        "profile": profile,
        "followers": followers,
        "following": following,
        "userFollowing": userFollowing
    })

def following_page(request):
    follow = Follow.objects.get(follower=request.user)
    following = follow.following.all()
    
    allPosts = Post.objects.all().order_by('-timestamp')
    posts = []
    for post in allPosts:
        if post.poster in following:
            posts.append(post)
        
    posts_paginator = Paginator(posts, 4)
    page_num = request.GET.get('page')
    page = posts_paginator.get_page(page_num)
    return render(request, "network/index.html", {
        "posts": page,
        "follow_page": True
    })

@csrf_exempt
def index(request):
    if request.method == "POST":
        content = request.POST["content"]
        post = Post(poster=request.user, content=content)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    elif request.method == "PUT":
        body = json.loads(request.body)
        if (body.get('like')):
            postid = int(body.get('postid'))
            post = Post.objects.get(pk=postid)

            post.likes.add(request.user)
            post.save()
        elif (body.get('unlike')):
            postid = int(body.get('postid'))
            post = Post.objects.get(pk=postid)

            post.likes.remove(request.user)
            post.save()
        else:
            content = body.get('content')
            postid = int(body.get('postid'))

            post = Post.objects.get(pk=postid)
            post.content = content
            post.save()

        return HttpResponse(status=204)

    posts = Post.objects.all().order_by('-timestamp')
    posts_paginator = Paginator(posts, 6)
    page_num = request.GET.get('page')
    page = posts_paginator.get_page(page_num)

    return render(request, "network/index.html", {
        "posts": page
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
