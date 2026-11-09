from django import forms
from .models import AdoptionApplication
from animal.models import Animal

class AdoptionForm(forms.ModelForm):
    class Meta:
        model = AdoptionApplication
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "postal_code",
            "reason_for_adoption"
        )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make all fields mandatory to proceed
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True
        self.fields["phone_number"].required = True
        self.fields["address_line_1"].required = True
        self.fields["address_line_2"].required = False
        self.fields["city"].required = True
        self.fields["state"].required = True
        self.fields["postal_code"].required = True
