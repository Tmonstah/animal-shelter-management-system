from django import forms
from datetime import date
from .models import Appointment


time_choices = [

    ("09:00", "9:00 AM"),
    ("09:30", "9:30 AM"),
    ("10:00", "10:00 AM"),
    ("10:30", "10:30 AM"),
    ("11:00", "11:00 AM"),
    ("11:30", "11:30 AM"),
    ("12:00", "12:00 PM"),
    ("12:30", "12:30 PM"),
    ("13:00", "1:00 PM"),
    ("13:30", "1:30 PM"),
    ("14:00", "2:00 PM"),
    ("14:30", "2:30 PM"),
    ("15:00", "3:00 PM"),
    ("15:30", "3:30 PM"),
    ("16:00", "4:00 PM"),
    ("16:30", "4:30 PM"),
]


class AppointmentForm(forms.ModelForm):
    appointment_time = forms.ChoiceField(
        choices=time_choices,
        label="Appointment Time",
    )


    class Meta:
        model = Appointment
        fields = (
            "appointment_date",
            "appointment_time",
        )

        widgets = {
            "appointment_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "appointment_time": forms.TimeInput(
                attrs={"type": "time"}
            ),
        }

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data["appointment_date"]

        if appointment_date < date.today():
            raise forms.ValidationError(
                "Appointment date cannot be in the past."
            )

        return appointment_date
