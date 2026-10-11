from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import EmployeeAccessRequest, EmployeeInvite, User
from django.utils import timezone

admin.site.register(User, UserAdmin) # this registers accounts.User model in the admin site & tells Django to use its built-in UserAdmin interface for it

admin.site.register(EmployeeInvite) # Allow superusers to create and manage employee invitation codes.

@admin.register(EmployeeAccessRequest) # Allow superusers to review employee access requests.
class EmployeeAccessRequestAdmin(admin.ModelAdmin):

    list_display = ( # Show Employee info
        "user",
        "status",
        "requested_at",
        "reviewed_at",
    )

    list_filter = ("status",) #Filter Status of Employee

    actions = ("approve_employee_requests", "deny_employee_requests") # Bulk updates

    @admin.action(description="Approve selected employee requests")
    def approve_employee_requests(self, request, queryset):
        for employee_request in queryset:
        # Give employee access as staff
            employee_request.user.is_staff = True
            employee_request.user.save()

        # Change status to approved and record timestamp
            employee_request.status = "approved"
            employee_request.reviewed_at = timezone.now()
            employee_request.save()

    @admin.action(description="Deny selected employee requests")
    def deny_employee_requests(self, request, queryset):
        for employee_request in queryset:
            # Keep the user as a normal customer account until further action is taken
            employee_request.user.is_staff = False
            employee_request.user.save()

            # Denial and Timestamp
            employee_request.status = "denied"
            employee_request.reviewed_at = timezone.now()
            employee_request.save()


    def save_model(self, request, obj, form, change):  # Synchronization to change status upon approval of request

        if obj.status == "approved":
            obj.user.is_staff = True
            obj.reviewed_at = timezone.now()

        elif obj.status == "denied":
            obj.user.is_staff = False
            obj.reviewed_at = timezone.now()

        obj.user.save()
        super().save_model(request, obj, form, change)
