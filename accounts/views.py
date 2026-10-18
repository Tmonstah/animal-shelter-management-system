from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import logout
from .forms import EmployeeProfileForm, CustomerProfileForm, CustomerRegistrationForm
from .models import EmployeeAccessRequest, EmployeeProfile, EmployeeInvite, CustomerProfile


def register_customer(request):
    if request.method == "POST":
        registration_form = CustomerRegistrationForm(request.POST)

        if registration_form.is_valid():
            user = registration_form.save()# Create the user account after all registration fields are validated.
            CustomerProfile.objects.create(user=user) # Create profile for every registered customer and collect metadata
            invite_code = registration_form.cleaned_data.get(   # Check whether the registrant supplied an employee invite code.
                "employee_invite_code"
            )

            if invite_code:
                employee_invite = EmployeeInvite.objects.get(   #Verfication of Invite and Email
                    invite_code=invite_code,
                    is_used=False,
                )

                EmployeeAccessRequest.objects.create(  # Change status to Pending for review of SuperUser
                    user=user,
                    invite=employee_invite,
                    status="pending",
                )

                # Prevent Duplicates.
                employee_invite.is_used = True
                employee_invite.save()

            return redirect("login")

    else:
        registration_form = CustomerRegistrationForm()

    return render(

        request,
        "accounts/register_customer.html",
        {"registration_form": registration_form},
    )



@login_required #this is to prevent false access to different pages
def customer_dashboard(request):
    if request.user.is_staff:
        return HttpResponseForbidden("Employees cannot access the customer portal.")

    return render(request, "accounts/customer_dashboard.html")


@login_required
def employee_dashboard(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Customers cannot access the employee portal.")

    return render(request, "accounts/employee_dashboard.html")

#Login Page Everyone taken here 
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect("/admin/")

            if user.is_staff:
                return redirect("employee_dashboard")

            return redirect("customer_dashboard")


        return render(
            request,
            "accounts/login.html",
            {"error_message": "Invalid username or password."},
        )

    return render(request, "accounts/login.html")

@login_required # this is to add meta data to the customer database
def customer_profile(request): # Employee access prvention Non-Functional
    if request.user.is_staff:
        return HttpResponseForbidden(
            "Employees cannot access the customer profile page."
        )

    customer_profile, created = CustomerProfile.objects.get_or_create( # Check if customer profile exist or else prompt to create
        user=request.user
    )

    if request.method == "POST":
        customer_profile_form = CustomerProfileForm(
            request.POST,
            instance=customer_profile,
        )

        if customer_profile_form.is_valid():
            customer_profile_form.save()
            return redirect("customer_profile")

    else:
        customer_profile_form = CustomerProfileForm(
            instance=customer_profile
        )
    #Display profile
    return render(
        request,
        "accounts/customer_profile.html",
        {
            "customer_profile_form": customer_profile_form,
        },
    )


@login_required
def employee_profile(request): # Customer access prvention Non-Functional
    if not request.user.is_staff:
        return HttpResponseForbidden(
            "Customers cannot access the employee profile page."
        )

    employee_profile, created = EmployeeProfile.objects.get_or_create( # Check if Employee profile exist or else prompt t>

        user=request.user
    )

    if request.method == "POST":
        employee_profile_form = EmployeeProfileForm(
            request.POST,
            instance=employee_profile,
        )

        if employee_profile_form.is_valid():
            employee_profile_form.save()
            return redirect("employee_profile")

    else:
        employee_profile_form = EmployeeProfileForm(
            instance=employee_profile
        )

    #Display Profile
    return render(
        request,
        "accounts/employee_profile.html",
        {
            "employee_profile_form": employee_profile_form,
        },
    )




def logout_view(request):
    logout(request)
    return redirect("login")
