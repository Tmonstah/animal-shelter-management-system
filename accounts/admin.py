from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


admin.site.register(User, UserAdmin) # this registers accounts.User model in the admin site & tells Django to use its built-in UserAdmin interface for it


