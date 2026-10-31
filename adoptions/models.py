from django.db import models
from accounts.models import CustomerProfile
from animal.models import Animal

# TODO add phone number type field. also update accounts

# This model is used to store adoption application information.
# The goal is that we want all applications to be associated with a 
# customer profile and a specific animal. If the customer does not have an account
# we would like the form to create one for them using the data in the application.
class AdoptionApplication(models.Model):
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