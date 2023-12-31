# parking_entry_app/models.py
from django.db import models
from django.contrib.auth.models import User

class ParkingEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plate_number = models.CharField(max_length=20)
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True, blank=True)
    vehicle_type = models.CharField(max_length=20, choices=[
        ('Car', 'Car'),
        ('Motorcycle', 'Motorcycle'),
        ('Truck', 'Truck'),
        ('Tricycle', 'Tricycle'),
        ('e-Bike', 'e-Bike'),
        ('Bicycle', 'Bicycle'),
    ])
    parking_fee = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=3, choices=[('IN', 'IN'), ('OUT', 'OUT')], default='IN')

    def __str__(self):
        return f"{self.plate_number} - {self.time_in}"
