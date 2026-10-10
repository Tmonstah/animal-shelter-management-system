from django.urls import path

from . import views


urlpatterns = [
    path("register/", views.register_customer, name="register_customer"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("customer/dashboard/", views.customer_dashboard, name="customer_dashboard"),
    path("employee/dashboard/", views.employee_dashboard, name="employee_dashboard"),
]
