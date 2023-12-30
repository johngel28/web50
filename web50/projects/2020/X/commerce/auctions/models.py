from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    watchlist = models.OneToOneField('Watchlist', on_delete=models.CASCADE, null=True, blank=True, related_name='user_watchlist')

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings_created")
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def close_auction(self):
        if not self.active:
            # The auction is already closed
            return
        self.active = False
        self.save()

    def __str__(self):
        return self.title

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    text = models.TextField()
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='user_watchlist')
    listings = models.ManyToManyField(Listing)

