# parking_entry_app/urls.py
from django.urls import path
from .views import parking_entry, transaction_history, user_admin, custom_login, custom_logout, ParkingEntryListView, exit_parking, TransactionHistoryListView, delete_entry, home
from . import views
urlpatterns = [
    path('', parking_entry, name='parking_entry'), 
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('transaction_history/', TransactionHistoryListView.as_view(), name='transaction_history'),
    path('user_admin/', user_admin, name='user_admin'),
    path('current_entries/', ParkingEntryListView.as_view(), name='parking_entry_list'),
    path('exit_parking/<int:entry_id>/', exit_parking, name='exit_parking'),  
    path('delete_entry/', views.delete_entry, name='delete_entry'),
    path('home/', home, name='home'),    
]
