from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "workshop"

urlpatterns = [
    path("workshop", RedirectView.as_view(pattern_name="workshop:home", permanent=False)),
    path("workshop/", views.home, name="home"),
    path("workshops/", views.workshop_list, name="list"),
    path("workshop/<slug:slug>/", views.workshop_detail, name="detail"),
]
