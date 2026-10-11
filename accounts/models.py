import secrets
import string

from django.contrib.auth.models import AbstractUser

from django.db import models

#User Model

class User(AbstractUser):
    pass
#Built in library to handle user data. General use case for everyone

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
