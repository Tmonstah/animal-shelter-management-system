from django import forms

from .models import MedicalRecord


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = (
            "record_type",
            "description",
            "record_date",
        )

        widgets = {
            "record_date": forms.DateInput(
                attrs={"type": "date"}
            ),
        }
