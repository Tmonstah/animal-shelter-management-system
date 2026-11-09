from django.db import models

from accounts.models import CustomerProfile, User
from animal.models import Animal


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    customer_profile = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name="appointments",
    )

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="appointments",
    )

    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_appointments",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.customer_profile.user.username} - "
            f"{self.animal.name} - "
            f"{self.appointment_date}"
        )
