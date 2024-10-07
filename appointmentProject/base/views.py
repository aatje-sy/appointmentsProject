from django.shortcuts import render, redirect
from .forms import AppointmentForm
from .models import Appointment
from .google_calendar import add_event_to_calendar
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()

            # Prepare event details for Google Calendar
            start_time = datetime.combine(appointment.date, appointment.time)
            end_time = start_time + timedelta(hours=1)  # Assuming each appointment lasts 1 hour
            
            # Add event to Google Calendar
            add_event_to_calendar(
                summary=f"Appointment with {request.user.username}",
                description=appointment.description,
                start_time=start_time.isoformat(),
                end_time=end_time.isoformat(),
            )

            return redirect('appointment_success')
    else:
        form = AppointmentForm()
    return render(request, 'base/book_appointment.html', {'form': form})

def appointment_success(request):
    return render(request, 'appointment_success.html')
