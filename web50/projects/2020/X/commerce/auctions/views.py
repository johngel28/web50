from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import ListingForm, BidForm
from .models import User, Listing, Bid, Comment, Watchlist, Category
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q
def index(request):
    # Retrieve all active listings
    active_listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {"listings": active_listings})

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
        
@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.created_by = request.user
            new_listing.current_bid = new_listing.starting_bid
            new_listing.save()

            # Add the listing to the user's watchlist
            watchlist, created = Watchlist.objects.get_or_create(user=request.user)
            watchlist.listings.add(new_listing)

            return redirect('active_listings')
    else:
        form = ListingForm()

    # Retrieve all categories to pass to the form
    categories = Category.objects.all()

    return render(request, 'auctions/create_listing.html', {'form': form, 'categories': categories})
    
@login_required
def my_listings(request):
    # Retrieve listings created by the current user
    my_listings = Listing.objects.filter(created_by=request.user)
    
    return render(request, 'auctions/my_listings.html', {'my_listings': my_listings})
def category_list(request):
    categories = Category.objects.all()
    return render(request, "auctions/category_list.html", {"categories": categories})

def active_listings(request):
    # Retrieve all active listings
    active_listings = Listing.objects.filter(active=True)

    # Handle search query
    query = request.GET.get('q')
    if query:
        active_listings = active_listings.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, "auctions/active_listings.html", {
        "listings": active_listings,
        "search_query": query,
    })
  
@login_required
def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    # Check if the user is the creator of the listing
    is_creator = listing.created_by == request.user

    # Handle bidding form submission
    if request.method == "POST" and "place_bid" in request.POST:
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            bid_amount = bid_form.cleaned_data["bid_amount"]
            # Validate bid amount
            if bid_conditions_met(listing, bid_amount):
                bid = Bid(amount=bid_amount, bidder=request.user, listing=listing)
                bid.save()
                listing.current_bid = bid_amount  # Update the current_bid field
                listing.save()
                messages.success(request, "Bid placed successfully!")
            else:
                messages.error(request, "Invalid bid amount.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        bid_form = BidForm()

    # Create or retrieve Watchlist instance for the user
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)

    # Handle watchlist actions
    is_watched = False
    if request.method == "POST" and "add_to_watchlist" in request.POST:
        watchlist.listings.add(listing)
        is_watched = True
    elif request.method == "POST" and "remove_from_watchlist" in request.POST:
        watchlist.listings.remove(listing)

    # Handle closing the auction
    if is_creator and request.method == "POST" and "close_auction" in request.POST:
        listing.close_auction()

    # Handle adding a comment
    if request.method == "POST" and "add_comment" in request.POST:
        comment_text = request.POST.get("comment_text")
        if comment_text:
            comment = Comment(text=comment_text, commenter=request.user, listing=listing)
            comment.save()

    # Retrieve all comments for the listing
    comments = Comment.objects.filter(listing=listing)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_watched": is_watched,
        "is_creator": is_creator,
        "comments": comments,
        "watchlist": watchlist,
        "bid_form": bid_form,
    })

def bid_conditions_met(listing, bid_amount):
    current_price = listing.current_bid or 0  # Set a default value if current_price is None
    return listing.active and bid_amount >= listing.starting_bid and bid_amount > current_price

@login_required
def watchlist(request):
    user = request.user

    # Create or retrieve Watchlist instance for the user
    watchlist, created = Watchlist.objects.get_or_create(user=user)

    listings = watchlist.listings.all()
    return render(request, "auctions/watchlist.html", {"listings": listings})

@login_required
def toggle_watchlist(request, listing_id):
    user = request.user

    # Retrieve Watchlist instance for the user, or create a new one if it doesn't exist
    watchlist, created = Watchlist.objects.get_or_create(user=user)

    listing = get_object_or_404(Listing, pk=listing_id)

    if listing in watchlist.listings.all():
        watchlist.listings.remove(listing)
    else:
        watchlist.listings.add(listing)

    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings = Listing.objects.filter(category=category)
    return render(request, "auctions/category_detail.html", {"category": category, "listings": listings}) 

def search(request):
    query = request.GET.get('q')
    if query:
        # Perform a case-insensitive search on the title and description fields
        results = Listing.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:
        results = []

    return render(request, 'auctions/search_results.html', {'query': query, 'results': results})    