from django.urls import path
from . import views
from .views import following_list

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("new-post/", views.new_post, name="new_post"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path('edit-post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('like-unlike-post/<int:post_id>/', views.like_unlike_post, name='like_unlike_post'),
    path('following/', following_list, name='following_list'),
    path('follow_unfollow/<str:username>/', views.follow_unfollow, name='follow_unfollow'),
    path('search/', views.search_users, name='search_users'),
]
