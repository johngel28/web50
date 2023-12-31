from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Post, Like
from .forms import NewPostForm 
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
@login_required
def like_unlike_post(request, post_id):
    try:
        print(f"Received request to like/unlike post {post_id}")
        # Get the post object or return a 404 response
        post = get_object_or_404(Post, pk=post_id)

        # Check if the user has already liked the post
        if request.user in post.likes.all():
            # User has liked the post; unlike it
            post.likes.remove(request.user)
            liked = False
        else:
            # User has not liked the post; like it
            post.likes.add(request.user)
            liked = True

        print(f"Post liked status: {liked}")
        # Return the updated like status
        return JsonResponse({'liked': liked})
    except Exception as e:
        print('Error:', e)
        return JsonResponse({'error': 'Internal Server Error'}, status=500)

def index(request):
    # Get all posts
    posts_list = Post.objects.all().order_by('-timestamp')

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        posts_list = posts_list.filter(Q(user__username__icontains=search_query) | Q(content__icontains=search_query))

    # Paginate the posts
    paginator = Paginator(posts_list, 10)  # Show 10 posts per page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request, "network/index.html", {"posts": posts, 'search_query': search_query})


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
@login_required
def new_post(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            user = request.user

            # Create a new post
            post = Post.objects.create(user=user, content=content)

            # Redirect to the home page or wherever you want to go after posting
            return redirect("index")
    else:
        form = NewPostForm()

    return render(request, "network/new_post.html", {"form": form})

@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(user=profile_user).order_by('-timestamp')

    # Pagination
    paginator = Paginator(user_posts, 10)  # Show 10 posts per page

    page = request.GET.get('page')
    try:
        user_posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        user_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results.
        user_posts = paginator.page(paginator.num_pages)

    # Check if the current user is following the profile user
    is_following = request.user.is_authenticated and request.user in profile_user.followers.all()

    # Display the number of followers and following count
    followers_count = profile_user.followers.count()
    following_count = profile_user.following.count()

    return render(request, "network/profile.html", {
        'profile_user': profile_user,
        'user_posts': user_posts,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    })

@login_required
def following(request):
    # Display posts from users that the current user follows
    following_users = request.user.following.all()
    following_posts = Post.objects.filter(user__in=following_users).order_by('-timestamp')

    return render(request, "network/following.html", {
        'following_posts': following_posts,
    })

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # Check if the logged-in user is the owner of the post
    if request.user == post.user:
        if request.method == "POST":
            # Process the form submission
            form = NewPostForm(request.POST)
            if form.is_valid():
                post.content = form.cleaned_data['content']
                post.save()
                return redirect("index")
        else:
            # For GET requests, populate the form with the existing post content
            form = NewPostForm(initial={'content': post.content})

        return render(request, "network/edit_post.html", {
            "post": post,
            "form": form,
        })

    # If the user is not the owner of the post, return an unauthorized response
    return HttpResponse("Unauthorized", status=401)


@login_required
def follow_unfollow(request, username):
    following_user = User.objects.get(username=username)

    if request.user != following_user:
        if request.user in following_user.followers.all():
            request.user.following.remove(following_user)
        else:
            request.user.following.add(following_user)

        # Redirect back to the user's profile page after the follow/unfollow operation
        return redirect('profile', username=username)
    else:
        # Redirect back to the user's profile page with a message indicating they can't follow themselves
        return redirect('profile', username=username, error_message="You cannot follow yourself")
        
@login_required
def following_list(request):
    following_users = request.user.following.all()
    return render(request, "network/following_list.html", {'following_users': following_users})
@login_required   
def search_users(request):
    query = request.GET.get('q')

    if not query:
        # No query provided, show error
        return render(request, 'network/search_users.html', {'error_message': 'Please enter a username'})

    # Perform a case-insensitive search for usernames containing the query
    results = User.objects.filter(Q(username__icontains=query))

    return render(request, 'network/search_users.html', {'results': results})