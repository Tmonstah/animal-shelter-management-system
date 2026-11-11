from django.urls import path

from . import views


urlpatterns = [
    path(
        "animals/<str:animal_id>/appointments/create/",
        views.appointment_create,
        name="appointment_create",
    ),

    path(
        "customer/appointments/",
        views.customer_appointments,
        name="customer_appointments",
    ),

    path(
    	"employee/appointments/",
    	views.employee_appointments,
    	name="employee_appointments",
    ),

    path(
    	"employee/appointments/<str:appointment_id>/approve/",
    	views.approve_appointment,
    	name="approve_appointment",
    ),

    path(
    	"employee/appointments/<str:appointment_id>/complete/",
    	views.complete_appointment,
    	name="complete_appointment",
    ),

    path(
    	"employee/appointments/<str:appointment_id>/cancel/",
    	views.cancel_appointment,
    	name="cancel_appointment",
    ),

    path(
    	"customer/appointments/history/",
    	views.previous_appointments,
    	name="previous_appointments",
    ),

]
