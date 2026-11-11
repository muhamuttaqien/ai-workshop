from django.urls import path

from . import views

app_name = "workshop"

urlpatterns = [
    path("", views.home, name="home"),
    path("workshops/", views.workshop_list, name="list"),
    path("workshop/<slug:slug>/", views.workshop_detail, name="detail"),
]
