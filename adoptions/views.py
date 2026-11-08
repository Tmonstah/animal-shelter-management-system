from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from .models import AdoptionApplication
from accounts.models import CustomerProfile
from animal.models import Animal
from django.utils import timezone
from .forms import AdoptionApplicationForm


@login_required
def adoption_application_create(request, animal_id):
    # Employees should not submit customer adoption applications.
    if request.user.is_staff:
        return HttpResponseForbidden(
            "Employees cannot submit adoption applications."
        )

    customer_profile, created = CustomerProfile.objects.get_or_create(
        user=request.user
    )

    animal = get_object_or_404(
        Animal,
        pk=animal_id,
        available=True,
    )

    existing_application = AdoptionApplication.objects.filter(
    	customer_profile=customer_profile,
    	animal_id=animal,
    	status="pending",
    ).exists()

    if existing_application:
    	return HttpResponseForbidden(
            "You already have a pending application for this animal."
    	)

    if request.method == "POST":
        application_form = AdoptionApplicationForm(request.POST)

        if application_form.is_valid():
            adoption_application = application_form.save(commit=False)

            # Connect the application to the logged-in customer and selected animal.
            adoption_application.customer_profile = customer_profile
            adoption_application.animal_id = animal

            adoption_application.save()

            return redirect("customer_dashboard")

    else:
        application_form = AdoptionApplicationForm(
            initial={
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
                "phone_num": customer_profile.phone_number,
                "address_line_1": customer_profile.address_line_1,
                "address_line_2": customer_profile.address_line_2,
                "city": customer_profile.city,
                "state": customer_profile.state,
                "postal_code": customer_profile.postal_code,
            }
        )

    return render(
        request,
        "adoptions/adoption_application_form.html",
        {
            "application_form": application_form,
            "animal": animal,
        },
    )

@login_required
def customer_adoption_applications(request):
    if request.user.is_staff:
        return HttpResponseForbidden(
            "Employees cannot access the customer adoption application page."
        )

    customer_profile = get_object_or_404(
        CustomerProfile,
        user=request.user,
    )

    adoption_applications = (
        customer_profile.adoption_applications
        .select_related("animal_id")
        .order_by("-submitted_at")
    )

    return render(
        request,
        "adoptions/customer_adoption_applications.html",
        {
            "adoption_applications": adoption_applications,
        },
    )

@login_required
def employee_adoption_applications(request):
    if not request.user.is_staff:
        return HttpResponseForbidden(
            "Customers cannot access employee adoption applications."
        )

    adoption_applications = AdoptionApplication.objects.order_by(
        "-submitted_at"
    )

    return render(
        request,
        "adoptions/employee_adoption_applications.html",
        {
            "adoption_applications": adoption_applications,
        },
    )

@login_required
def approve_adoption_application(request, application_id):
    if not request.user.is_staff:
        return HttpResponseForbidden(
            "Customers cannot approve adoption applications."
        )

    adoption_application = get_object_or_404(
        AdoptionApplication,
        pk=application_id,
    )

    if request.method == "POST":
        adoption_application.status = "approved"
        adoption_application.reviewed_by = request.user
        adoption_application.reviewed_at = timezone.now()
        adoption_application.save()

        # Mark the animal as unavailable once an application is approved.
        animal = adoption_application.animal_id
        animal.available = False
        animal.save()

    return redirect("employee_adoption_applications")


@login_required
def deny_adoption_application(request, application_id):
    if not request.user.is_staff:
        return HttpResponseForbidden(
            "Customers cannot deny adoption applications."
        )

    adoption_application = get_object_or_404(
        AdoptionApplication,
        pk=application_id,
    )

    if request.method == "POST":
        adoption_application.status = "denied"
        adoption_application.reviewed_by = request.user
        adoption_application.reviewed_at = timezone.now()
        adoption_application.save()

    return redirect("employee_adoption_applications")
