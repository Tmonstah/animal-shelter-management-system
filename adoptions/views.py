from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import logout
from .forms import AdoptionForm
from .models import AdoptionApplication
from accounts.models import CustomerProfile
from animal.models import Animal
from django.utils import timezone
from django.db.models import Case, When, Value, CharField

# We only want people who have accounts to fill out applications
# easier for tracking them.
@login_required 
def adoption_form_view(request, pk):
    # Verify that customer does not have an application for the current animal
    customer_profile = CustomerProfile.objects.get(
        user=request.user
    )
    animal_id = get_object_or_404(
        Animal,
        pk=pk,
        available="available",
    )
    existing_application = AdoptionApplication.objects.filter(
    	customer_profile=customer_profile,
    	animal=animal_id.pk,
    	status="pending",
    ).exists()

    if existing_application:
        return HttpResponseForbidden(
            "You already have a pending application for this animal."
        )

    # If user is submitting the form
    if request.method == "POST":
        adoption_form = AdoptionForm(request.POST)

        #Check that the form is valid, and then save the application
        if adoption_form.is_valid():
            application = adoption_form.save(commit=False)
            # Add in the user info that is not seen on form
            application.customer_profile = request.user.customer_profile
            application.animal = animal_id
            application.save()
            return render(
                request,
                "adoption_application_success.html",
                {"adoption_application_form": application, "animal": animal_id,},
            )

    else: 
        # Check if user is logged in and not a staff account, if so fill in all info
        #   based on the account info.
        if request.user.is_authenticated and not request.user.is_staff:
            cust_profile = request.user.customer_profile
            adoption_form = AdoptionForm(initial={
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
                "phone_number": cust_profile.phone_number,
                "address_line_1": cust_profile.address_line_1,
                "address_line_2": cust_profile.address_line_2,
                "city": cust_profile.city,
                "state": cust_profile.state,
                "postal_code": cust_profile.postal_code,
                "animal": pk,
            })

        # We only want customer accounts to fill out applications, no staff.
        else: 
            return render(
                request,
                "customer_account_only_error.html",
                status=403
            )

    return render(
            request,
            "adoption_application.html",
            {"adoption_application_form": adoption_form, "animal": animal_id,},
    )

# This is the view for customers to see all their applications
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
    order_status = Case(
        When(status= "approved", then= Value("b")),
        When(status= "denied", then= Value("c")),
        When(status= "pending", then= Value("a")),
        default= Value("d"),
        output_field= CharField()
    )

    adoption_applications = (
        customer_profile.adoption_applications
        .select_related("animal")
        .order_by(order_status, "-submitted_at")
    )

    return render(
        request,
        "customer_adoption_applications.html",
        {
            "adoption_applications": adoption_applications,
        },
    )

# This view is for the employee to see all the applications in the system
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

# Allow the manager to approve animal applications            
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
        animal.available = 'unavailable'
        animal.save()

    return redirect("employee_adoption_applications")

# Allow a manager to deny an application            
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
