from django.db import models

# User Model

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


#AbstractUser native attributes: username, email, password, first/last name, is_staff, is_superuser, groups, permissions, active status
