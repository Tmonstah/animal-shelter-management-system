from django import forms

from .models import AdoptionApplication


class AdoptionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdoptionApplication
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_num",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "postal_code",
            "reason_for_adoption",
        )
