from django.urls import path
from . import views

urlpatterns = [
    path("", views.animal_listing, name="animals_list"),
]