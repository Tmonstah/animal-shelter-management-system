from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("customer/dashboard/", views.customer_dashboard, name="customer_dashboard"),
    path("employee/dashboard/", views.employee_dashboard, name="employee_dashboard"),
    path("logout/", views.logout_view, name="logout"),
]
