"""URL configuration for the core project.

Includes the admin site and the API routes contributed by each app.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("auth_app.api.urls")),
]
