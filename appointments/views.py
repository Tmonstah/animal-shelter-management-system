from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.models import CustomerProfile
from animal.models import Animal

from .forms import AppointmentForm
from .models import Appointment


@login_required
def appointment_create(request, animal_id):
    if request.user.is_staff:
        return HttpResponseForbidden(
            "Employees cannot create customer appointments."
        )

    customer_profile, created = CustomerProfile.objects.get_or_create(
        user=request.user
    )

    animal = get_object_or_404(
        Animal,
        pk=animal_id,
        available='available',
    )

    if request.method == "POST":
        appointment_form = AppointmentForm(request.POST)

        if appointment_form.is_valid():
            appointment_date = appointment_form.cleaned_data["appointment_date"]
            appointment_time = appointment_form.cleaned_data["appointment_time"]

            # Prevent two appointments from using the same time slot.
            time_slot_taken = Appointment.objects.filter(
                appointment_date=appointment_date,
                appointment_time=appointment_time,
            ).exclude(
                status="cancelled"
            ).exists()

            if time_slot_taken:
                appointment_form.add_error(
                    None,
                    "This appointment time is already booked."
                )

            else:
                appointment = appointment_form.save(commit=False)

                appointment.customer_profile = customer_profile
                appointment.animal = animal
                appointment.save()

                return redirect("customer_appointments")

    else:
        appointment_form = AppointmentForm()

    return render(
        request,
        "appointments/appointment_form.html",
        {
            "appointment_form": appointment_form,
            "animal": animal,
        },
    )


@login_required
def customer_appointments(request):
    if request.user.is_staff:
        return HttpResponseForbidden(
            "Employees cannot access the customer appointments page."
        )

    customer_profile = get_object_or_404(
        CustomerProfile,
        user=request.user,
    )

    upcoming_appointments = (
        customer_profile.appointments
        .filter(status__in=["pending", "approved"], appointment_date__gte=timezone.localdate())
        .select_related("animal")
        .order_by("appointment_date", "appointment_time")
    )


    return render(
        request,
        "appointments/customer_appointments.html",
        {
            "upcoming_appointments": upcoming_appointments,
        },
    )

#This view is to show all previous appointments for the customer shows both completed and canceled

@login_required
def previous_appointments(request):
    if request.user.is_staff:
        return HttpResponseForbidden(
            "Employees cannot access the customer appointment history page."
        )

    customer_profile = get_object_or_404(
        CustomerProfile,
        user=request.user,
    )

    previous_appointments = (
        customer_profile.appointments
        .filter(status__in=["completed", "cancelled"],appointment_date__lt=timezone.localdate())
        .select_related("animal")
        .order_by("-appointment_date", "-appointment_time")
    )

    return render(
        request,
        "appointments/previous_appointments.html",
        {
            "previous_appointments": previous_appointments,
        },
    )

@login_required
def employee_appointments(request):
    if not request.user.is_staff:
        return HttpResponseForbidden(
            "Customers cannot access employee appointment management."
        )

    appointments = Appointment.objects.order_by(
        "appointment_date",
        "appointment_time",
    )

    return render(
        request,
        "appointments/employee_appointments.html",
        {
            "appointments": appointments,
        },
    )

@login_required
def approve_appointment(request, appointment_id):
    if not request.user.is_staff:
        return HttpResponseForbidden(
            "Customers cannot approve appointments."
        )

    appointment = get_object_or_404(
        Appointment,
        pk=appointment_id,
    )

    if request.method == "POST":
        appointment.status = "approved"
        appointment.reviewed_by = request.user
        appointment.save()

    return redirect("employee_appointments")


@login_required
def complete_appointment(request, appointment_id):
    if not request.user.is_staff:
        return HttpResponseForbidden(
            "Customers cannot complete appointments."
        )

    appointment = get_object_or_404(
        Appointment,
        pk=appointment_id,
    )

    if request.method == "POST":
        appointment.status = "completed"
        appointment.reviewed_by = request.user
        appointment.save()

    return redirect("employee_appointments")


@login_required
def cancel_appointment(request, appointment_id):
    if not request.user.is_staff:
        return HttpResponseForbidden(
            "Customers cannot cancel appointments."
        )

    appointment = get_object_or_404(
        Appointment,
        pk=appointment_id,
    )

    if request.method == "POST":
        appointment.status = "cancelled"
        appointment.reviewed_by = request.user
        appointment.save()

    return redirect("employee_appointments")
