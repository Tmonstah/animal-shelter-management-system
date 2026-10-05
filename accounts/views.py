from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import logout

@login_required
def customer_dashboard(request):
    if request.user.is_staff:
        return HttpResponseForbidden("Employees cannot access the customer portal.")

    return render(request, "accounts/customer_dashboard.html")


@login_required
def employee_dashboard(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Customers cannot access the employee portal.")

    return render(request, "accounts/employee_dashboard.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_staff:
                return redirect("employee_dashboard")

            return redirect("customer_dashboard")

        return render(
            request,
            "accounts/login.html",
            {"error_message": "Invalid username or password."},
        )

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")
