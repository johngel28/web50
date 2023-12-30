from django.urls import path
from .views import (
    index, login_view, logout_view, register, create_listing, 
    active_listings, listing, watchlist, toggle_watchlist, 
    category_list, category_detail, my_listings, search
)

urlpatterns = [
    path("", index, name="index"),
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("register", register, name="register"),

    path("create_listing", create_listing, name="create_listing"),
    path("active_listings", active_listings, name="active_listings"),
    path("listing/<int:listing_id>", listing, name="listing"),
    path("watchlist", watchlist, name="watchlist"),
    path("toggle_watchlist/<int:listing_id>", toggle_watchlist, name="toggle_watchlist"),
    path('categories/', category_list, name='category_list'),
    path('category/<int:category_id>/', category_detail, name='category_detail'),
    path('my_listings', my_listings, name='my_listings'),
    path('search/', search, name='search'),
]

