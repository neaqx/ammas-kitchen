from django.shortcuts import render, redirect, get_object_or_404
from .models import Reservation, Table
from .forms import ReservationForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages

# Startseite
def home(request):
    return render(request, 'reservations/home.html')

# View für das Erstellen einer Reservierung
@login_required
def make_reservation(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            conflicting_reservations = Reservation.objects.filter(
                table=reservation.table, date=reservation.date, time=reservation.time
            )
            if conflicting_reservations.exists():
                messages.error(request, 'Double booking! Please choose another time or table.')
                return render(request, 'reservations/reservation_form.html', {'form': form})
            
            reservation.user = request.user
            reservation.save()
            messages.success(request, 'Reservation successfully created!')
            return redirect('my_reservations')
    else:
        form = ReservationForm()

    return render(request, 'reservations/reservation_form.html', {'form': form})

# View zur Anzeige der Reservierungen des Benutzers
@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'reservations/my_reservations.html', {'reservations': reservations})

# View zum Stornieren einer Reservierung
@login_required
def cancel_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    
    if reservation.user == request.user:
        reservation.delete()
        messages.success(request, 'Reservation successfully canceled!')
    else:
        messages.error(request, 'You are not authorized to cancel this reservation.')

    return redirect('my_reservations')

# View zur Benutzerregistrierung
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Amma\'s Kitchen.')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})




