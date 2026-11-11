from django.contrib import admin
from django.urls import include, path

from .admin_sites import courses_admin_site, workshop_admin_site


urlpatterns = [
    path("admin-courses/", courses_admin_site.urls),
    path("admin-workshop/", workshop_admin_site.urls),
    path("admin/", admin.site.urls),  # Legacy admin address remains accessible.
    path("", include("courses.urls")),
    path("", include("workshop.urls")),
]
