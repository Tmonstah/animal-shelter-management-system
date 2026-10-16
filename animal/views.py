# Create your views here.
from django.shortcuts import render

from .forms import AnimalFilterForm
from .models import Animal


def animal_list(request):
    filter_form = AnimalFilterForm(request.GET or None)
    available_animals = Animal.objects.filter(available=True)

    if filter_form.is_valid():
        filters = filter_form.cleaned_data
        if filters["breed"]:
            available_animals = available_animals.filter(breed=filters["breed"])
        if filters["gender"]:
            available_animals = available_animals.filter(gender=filters["gender"])
        if filters["min_age"] is not None:
            available_animals = available_animals.filter(age__gte=filters["min_age"])
        if filters["max_age"] is not None:
            available_animals = available_animals.filter(age__lte=filters["max_age"])

    return render(
        request,
        "shelter_project/animal_listing.html",
        {"animals": available_animals, "filter_form": filter_form},
    )
