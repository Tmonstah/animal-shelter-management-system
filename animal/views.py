# Create your views here.
from django.contrib.auth.decorators import login_required
from django.db.models import Case, IntegerField, Value, When
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AnimalCreateForm, AnimalFilterForm, AnimalUpdateForm
from .models import Animal

MAX_AVAILABLE_ANIMALS = 50


def animal_list(request):
    staff_view = request.user.is_authenticated and (
        request.user.is_staff or request.user.is_superuser
    )
    filter_form = AnimalFilterForm(
        request.GET or None,
        include_unavailable=staff_view,
    )
    animals = Animal.objects.all()
    if not staff_view:
        animals = animals.filter(available="available")

    if filter_form.is_valid():
        filters = filter_form.cleaned_data
        if filters["name"]:
            animals = animals.filter(
                name__icontains=filters["name"]
            )
        if filters["animal_type"]:
            animals = animals.filter(animal_type=filters["animal_type"])
        if filters["breed"]:
            animals = animals.filter(breed=filters["breed"])
        if filters["gender"]:
            animals = animals.filter(gender=filters["gender"])
        if filters["min_age"] is not None:
            animals = animals.filter(age__gte=filters["min_age"])
        if filters["max_age"] is not None:
            animals = animals.filter(age__lte=filters["max_age"])

    if staff_view:
        animals = animals.order_by(
            Case(
                When(available="pending", then=Value(0)),
                When(available="available", then=Value(1)),
                When(available="unavailable", then=Value(2)),
                default=Value(3),
                output_field=IntegerField(),
            ),
            "name",
            "pk",
        )
    else:
        animals = animals.order_by("name", "pk")

    return render(
        request,
        "shelter_project/animal_listing.html",
        {"animals": animals, "filter_form": filter_form, "staff_view": staff_view},
    )


@login_required
def animal_create(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden(
            "Only employees and managers can add animals."
        )

    available_count = Animal.objects.filter(available="available").count()
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
    animal_query = Animal.objects.all().prefetch_related("medical_records")
    animal = get_object_or_404(animal_query, pk=animal_id)
    return render(
        request,
        "shelter_project/animal_detail.html",
        {"animal": animal},
    )


@login_required
def animal_edit(request, animal_id):
    if not (request.user.is_superuser or request.user.is_staff):
        return HttpResponseForbidden("Only managers can edit animal profiles.")

    animal = get_object_or_404(Animal, pk=animal_id)
    was_available = animal.available == "available"
    if request.method == "POST":
        form = AnimalUpdateForm(request.POST, request.FILES, instance=animal)
        if form.is_valid():
            becomes_available = (
                not was_available
                and form.cleaned_data["available"] == "available"
            )
            available_count = Animal.objects.filter(available="available").count()
            if becomes_available and available_count >= MAX_AVAILABLE_ANIMALS:
                form.add_error(
                    "available",
                    "The shelter already has the maximum of 50 available animals.",
                )
            else:
                form.save()
                return redirect("animal_list")
    else:
        form = AnimalUpdateForm(instance=animal)

    return render(
        request,
        "shelter_project/animal_edit.html",
        {"animal": animal, "form": form},
    )
