# parking_entry_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import ParkingEntry
from django.views.generic import ListView
from django.utils import timezone
from .forms import TransactionSearchForm  # Add this import
from django.db.models import Q  # Add this import for query condition

class ParkingEntryListView(ListView):
    model = ParkingEntry
    template_name = 'parking_entry_app/parking_entry_list.html'
    context_object_name = 'entries'

    def get_queryset(self):
        return ParkingEntry.objects.filter(user=self.request.user, time_out__isnull=True)
def delete_entry(request):
    if request.method == 'GET':
        entry_id = request.GET.get('entry_id')
        entry = get_object_or_404(ParkingEntry, id=entry_id, user=request.user)

        # Assuming you want to perform the deletion here
        entry.delete()

    return redirect('parking_entry')  # Redirect to the appropriate page after deletion
def exit_parking(request, entry_id):
    entry = get_object_or_404(ParkingEntry, id=entry_id, user=request.user)

    if entry.status == 'IN':
        entry.status = 'OUT'
        entry.time_out = timezone.now()
        entry.save()

    return redirect('parking_entry')

def user_admin(request):
    if request.method == 'POST' and 'change_password' in request.POST:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update session to avoid re-login
            return redirect('parking_entry')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'parking_entry_app/user_admin.html', {'form': form})

def parking_entry(request):
    if request.method == 'POST':
        plate_number = request.POST.get('plate_number')
        vehicle_type = request.POST.get('vehicle_type')
        time_in = timezone.now()
        parking_fee = calculate_parking_fee(vehicle_type)

        entry = ParkingEntry(
            user=request.user,
            plate_number=plate_number,
            time_in=time_in,
            vehicle_type=vehicle_type,
            parking_fee=parking_fee
        )
        entry.save()

    entries = ParkingEntry.objects.filter(user=request.user, time_out__isnull=True)
    return render(request, 'parking_entry_app/parking_entry.html', {'entries': entries})

def calculate_parking_fee(vehicle_type):
    fee_mapping = {
        'Car': 50,
        'Motorcycle': 30,
        'Truck': 0,  # Adjust as needed
        'Tricycle': 40,
        'e-Bike': 30,
        'Bicycle': 20,
    }
    return fee_mapping.get(vehicle_type, 0)


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('parking_entry')
    return render(request, 'home.html')
    

def change_password(request):
    if request.method == 'POST' and 'change_password' in request.POST:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update session to avoid re-login
            return redirect('parking_entry')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'parking_entry_app/change_password.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('home')
def transaction_history(request):
    form = TransactionSearchForm(request.GET)
    entries = ParkingEntry.objects.filter(user=request.user)
    print("THESE ARE YOUR ENTRIES", entries)
    if form.is_valid():
        plate_number = form.cleaned_data.get('plate_number')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        status = form.cleaned_data.get('status')

        entries = entries.filter(
            Q(plate_number__icontains=plate_number) |
            Q(time_in__gte=start_date) |
            Q(time_out__lte=end_date) |
            Q(status=status) if status else Q()
        )

    return render(request, 'parking_entry_app/transaction_history.html', {'form': form, 'entries': entries})
def home(request):
    if request.user.is_authenticated:
        entries = ParkingEntry.objects.filter(user=request.user, time_out__isnull=True)
        print(entries)  # Add this line to print entries to the console
        return render(request, 'home.html', {'entries': entries})
    else:
        return render(request, 'home.html')

class TransactionHistoryListView(ListView):
    model = ParkingEntry
    template_name = 'parking_entry_app/transaction_history.html'
    context_object_name = 'entries'
    ordering = ['-time_in']

    def get_queryset(self):
        queryset = ParkingEntry.objects.filter(user=self.request.user)
        search_query = self.request.GET.get('search')

        if search_query:
            queryset = queryset.filter(
                Q(plate_number__icontains=search_query) |
                Q(vehicle_type__icontains=search_query) |
                Q(status__icontains=search_query)
            )

        return queryset


