from django.db import models

from accounts.models import User
from animal.models import Animal


class MedicalRecord(models.Model):
    RECORD_TYPE_CHOICES = [
        ("checkup", "Checkup"),
        ("vaccination", "Vaccination"),
        ("medication", "Medication"),
        ("injury", "Injury"),
        ("other", "Other"),
    ]

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="medical_records",
    )

    record_type = models.CharField(
        max_length=20,
        choices=RECORD_TYPE_CHOICES,
        default="other",
    )

    description = models.TextField()

    record_date = models.DateField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_medical_records",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.animal.name} - "
            f"{self.record_type} - "
            f"{self.record_date}"
        )
