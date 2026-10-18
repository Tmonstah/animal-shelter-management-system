import secrets
import string

from django.contrib.auth.models import AbstractUser

from django.db import models

#User Model
#Built in library to handle user data. General use case for everyone

class User(AbstractUser):
    pass

#This class is to add a profile display for the customer tied to the back end metadata

class CustomerProfile(models.Model):
    # Customer Front to Back 1:1

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="customer_profile",
    )

    # Customer Meta data
    phone_number = models.CharField(max_length=20, blank=True)
    address_line_1 = models.CharField(max_length=150, blank=True)
    address_line_2 = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} Customer Profile"

class EmployeeProfile(models.Model): # Front to Backend connection 1:1
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="employee_profile",
    )

    # Employee MetaData
    phone_number = models.CharField(max_length=20, blank=True)
    employee_id = models.CharField(max_length=50, unique=True)
    job_title = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    hire_date = models.DateField(null=True, blank=True)


    # TimeStamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user.username} Employee Profile"


def generate_invite_code():

    characters = string.ascii_uppercase + string.digits
    random_part = "".join(secrets.choice(characters) for _ in range(6))

    return f"EMP-{random_part}"
#Function to generate unique employee invite code

class EmployeeInvite(models.Model):
    email = models.EmailField(unique=True)
    invite_code = models.CharField(

        max_length=20,
        unique=True,
        default=generate_invite_code,
        editable=False,

    )

    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.invite_code}"
#Class to create invite for Onboarding new employee

class EmployeeAccessRequest(models.Model):
    STATUS_CHOICES = [
        
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("denied", "Denied"),
    
    ]

    user = models.OneToOneField(
    
        User,
        on_delete=models.CASCADE,
        related_name="employee_access_request",
    
    )

    invite = models.OneToOneField(
    
        EmployeeInvite,
        on_delete=models.CASCADE,
        related_name="access_request",
    
    )

    status = models.CharField(
        
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
    
    )

    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"

#Class to handle employee approval request for gaining access to features.
#This is handled on the SuperUser side 
# None is for anyone
#Pending is for amployees who have used the invite code to register and waiting for approval
#Approved is when Superuser has approved employee onboarding 
