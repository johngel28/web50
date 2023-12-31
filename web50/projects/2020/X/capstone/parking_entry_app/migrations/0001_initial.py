# Generated by Django 5.0 on 2023-12-31 14:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ParkingEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plate_number', models.CharField(max_length=20)),
                ('time_in', models.DateTimeField(auto_now_add=True)),
                ('time_out', models.DateTimeField(blank=True, null=True)),
                ('vehicle_type', models.CharField(choices=[('Car', 'Car'), ('Motorcycle', 'Motorcycle'), ('Truck', 'Truck'), ('Tricycle', 'Tricycle'), ('e-Bike', 'e-Bike'), ('Bicycle', 'Bicycle')], max_length=20)),
                ('parking_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
