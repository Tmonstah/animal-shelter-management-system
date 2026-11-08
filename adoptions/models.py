from django.db import models

from accounts.models import CustomerProfile, User
from animal.models import Animal


class AdoptionApplication(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("denied", "Denied"),
    ]

    customer_profile = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name="adoption_applications",
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=False)
    phone_num = models.CharField(max_length=20, blank=True)

    address_line_1 = models.CharField(max_length=150, blank=True)
    address_line_2 = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    animal_id = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="adoption_applications",
    )

    reason_for_adoption = models.TextField(blank=True)

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
        related_name="reviewed_adoption_applications",
    )

    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return (
            f"{self.first_name} {self.last_name} - "
            f"{self.animal_id.name} - {self.status}"
        )
