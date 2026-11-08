from django.urls import path

from . import views


urlpatterns = [
    path(
        "animals/<str:animal_id>/medical/",
        views.animal_medical_records,
        name="animal_medical_records",
    ),

    path(
        "animals/<str:animal_id>/medical/add/",
        views.medical_record_create,
        name="medical_record_create",
    ),
]
