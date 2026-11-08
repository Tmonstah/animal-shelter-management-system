from django.urls import path

from . import views


urlpatterns = [
    path(
        "animals/<str:animal_id>/apply/",
        views.adoption_application_create,
        name="adoption_application_create",
    ),

    path(
        "customer/applications/",
        views.customer_adoption_applications,
        name="customer_adoption_applications",
    ),

    path(
   	"employee/applications/",
    	views.employee_adoption_applications,
    	name="employee_adoption_applications",
    ),

    path(
    	"employee/applications/<str:application_id>/approve/",
    	views.approve_adoption_application,
    	name="approve_adoption_application",
    ),

    path(
    	"employee/applications/<str:application_id>/deny/",
    	views.deny_adoption_application,
    	name="deny_adoption_application",
    ),

]
