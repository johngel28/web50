# parking_entry_app/admin.py
from django.contrib import admin
from .models import ParkingEntry

@admin.register(ParkingEntry)
class ParkingEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'plate_number', 'time_in', 'time_out', 'vehicle_type', 'status']
    search_fields = ['user__username', 'plate_number']
    list_filter = ['vehicle_type', 'status']
    ordering = ['-time_in']
