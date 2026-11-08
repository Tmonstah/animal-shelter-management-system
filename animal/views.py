# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AnimalCreateForm, AnimalFilterForm
from .models import Animal

MAX_AVAILABLE_ANIMALS = 50


def animal_list(request):
    filter_form = AnimalFilterForm(request.GET or None)
    available_animals = Animal.objects.filter(available="available")

    if filter_form.is_valid():
        filters = filter_form.cleaned_data
        if filters["name"]:
            available_animals = available_animals.filter(
                name__icontains=filters["name"]
            )
        if filters["animal_type"]:
            available_animals = available_animals.filter(animal_type=filters["animal_type"])
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


@login_required
def animal_create(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden(
            "Only employees and managers can add animals."
        )

    available_count = Animal.objects.filter(available=True).count()
    if request.method == "POST":
        form = AnimalCreateForm(request.POST, request.FILES)
        if available_count >= MAX_AVAILABLE_ANIMALS:
            form.add_error(
                None,
                "The shelter already has the maximum of 50 available animals.",
            )
        # Keep in mind ModelForm and form relationship. This validation will also
        # run animal validations.
        elif form.is_valid():
            form.save()
            return redirect("animal_list")
    else:
        form = AnimalCreateForm()
    # Fall through logic for rendering the default form
    return render(
        request,
        "shelter_project/animal_create.html",
        {
            "form": form,
            "at_capacity": available_count >= MAX_AVAILABLE_ANIMALS,
        },
    )


def animal_detail(request, animal_id):
    animal = get_object_or_404(Animal, pk=animal_id, available=True)
    return render(
        request,
        "shelter_project/animal_detail.html",
        {"animal": animal_id},
    )
