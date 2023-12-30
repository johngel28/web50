# auctions/admin.py
from django.contrib import admin
from .models import Listing, Bid, Comment, Category, Watchlist

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'starting_bid', 'current_bid', 'created_by', 'created_at', 'active']
    search_fields = ['title', 'created_by__username']

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['listing', 'bidder', 'amount', 'created_at']
    search_fields = ['listing__title', 'bidder__username']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'commenter', 'listing']
    search_fields = ['text', 'commenter__username', 'listing__title']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_listings']

    def get_listings(self, obj):
        return ', '.join([listing.title for listing in obj.listings.all()])
    
    get_listings.short_description = 'Listings'
    search_fields = ['user__username']
