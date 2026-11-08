"""
URL configuration for shelter_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from shelter_project import views as shelter_views
from animal import views as animal_views
from accounts import views as account_views


urlpatterns = [
    # Override the default Django admin logout.
    path(
        "admin/logout/",
        account_views.logout_view,
        name="admin_logout_redirect",
    ),

    # Django administration page.
    path("admin/", admin.site.urls),

    # Animal pages.
    path("animals/", animal_views.animal_list, name="animal_list"),
    path("animals/add/", animal_views.animal_create, name="animal_create"),
    path(
        "animals/<str:animal_id>/",
        animal_views.animal_detail,
        name="animal_detail",
    ),

    # Main project pages.
    path("home/", shelter_views.home, name="home"),

    # Account and adoption routes.
    path("", include("accounts.urls")),
    path("", include("adoptions.urls")),
    path("", include("appointments.urls")),
    path("", include("medical.urls")),
]


# Allows uploaded animal images to display during development.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
