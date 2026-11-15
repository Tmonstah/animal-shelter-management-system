from django.contrib import admin
from .models import AdoptionApplication


class AdoptionApplicationAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if obj.status == "approved":
            obj.animal.available = "adopted"

        if obj.status == "denied":
            obj.animal.available = "available"

        if obj.status == "pending":
            obj.animal.available = "pending"

        obj.animal.save()
        super().save_model(request, obj, form, change)

admin.site.register(AdoptionApplication, AdoptionApplicationAdmin)