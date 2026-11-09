from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from animal.models import Animal

from .forms import MedicalRecordForm
from .models import MedicalRecord


@login_required
def medical_record_create(request, animal_id):
    if not request.user.is_staff:
        return HttpResponseForbidden(
            "Only employees can add medical records."
        )

    animal = get_object_or_404(
        Animal,
        pk=animal_id,
    )

    if request.method == "POST":
        medical_record_form = MedicalRecordForm(request.POST)

        if medical_record_form.is_valid():
            medical_record = medical_record_form.save(commit=False)
            medical_record.animal = animal
            medical_record.created_by = request.user
            medical_record.save()

            return redirect(
                "animal_medical_records",
                animal_id=animal.id,
            )

    else:
        medical_record_form = MedicalRecordForm()

    return render(
        request,
        "medical/medical_record_form.html",
        {
            "medical_record_form": medical_record_form,
            "animal": animal,
        },
    )


@login_required
def animal_medical_records(request, animal_id):
    if not request.user.is_staff:
        return HttpResponseForbidden(
            "Only employees can view full medical records."
        )

    animal = get_object_or_404(
        Animal,
        pk=animal_id,
    )

    medical_records = MedicalRecord.objects.filter(
        animal=animal
    ).order_by("-record_date")

    return render(
        request,
        "medical/animal_medical_records.html",
        {
            "animal": animal,
            "medical_records": medical_records,
        },
    )
