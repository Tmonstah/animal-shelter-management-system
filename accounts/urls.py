from django.urls import path

from . import views

#This is pretty straight forward Just the urls and paths

urlpatterns = [
    path("register/", views.register_customer, name="register_customer"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("customer/dashboard/", views.customer_dashboard, name="customer_dashboard"),
    path("employee/dashboard/", views.employee_dashboard, name="employee_dashboard"),
    path("customer/profile/", views.customer_profile, name="customer_profile"),
    path("employee/profile/", views.employee_profile, name="employee_profile"),
]
