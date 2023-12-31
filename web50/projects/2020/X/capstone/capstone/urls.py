# capstone/urls.py
from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('parking/', include('parking_entry_app.urls')),
    path('', home, name='home'),  # Add this line for the default view
]
