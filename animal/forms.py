from django import forms

from .models import Animal


class AnimalFilterForm(forms.Form):
    breed = forms.ChoiceField(required=False, label="Breed")
    gender = forms.ChoiceField(required=False, label="Gender")
    min_age = forms.IntegerField(required=False, min_value=0, label="Minimum age")
    max_age = forms.IntegerField(required=False, min_value=0, label="Maximum age")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        breeds = (
            Animal.objects.filter(available=True)
            .order_by("breed")
            .values_list("breed", flat=True)
            .distinct()
        )
        self.fields["breed"].choices = [("", "All breeds")] + [
            (breed, breed) for breed in breeds
        ]
        self.fields["gender"].choices = [("", "All genders")] + list(
            Animal.ANIMAL_GENDER_CHOICES.items()
        )

    def clean(self):
        cleaned_data = super().clean()
        min_age = cleaned_data.get("min_age")
        max_age = cleaned_data.get("max_age")

        if min_age is not None and max_age is not None and min_age > max_age:
            self.add_error("max_age", "Maximum age must be at least the minimum age.")

        return cleaned_data
