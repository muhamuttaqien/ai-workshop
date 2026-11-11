from collections import OrderedDict

from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Testimonial, Workshop


WORKSHOP_PREFETCHES = (
    "intro_paragraph_items",
    "outcome_items",
    "audience_items",
    "curriculum_items",
    "benefit_items",
    "schedule_items",
    "faq_items",
)


def _registration_url(workshop):
    if workshop.registration_url:
        return workshop.registration_url
    return getattr(settings, "WORKSHOP_REGISTRATION_URL", "#")


def _recording_request_url():
    return (
        getattr(settings, "WORKSHOP_RECORDING_REQUEST_URL", "")
        or getattr(settings, "WORKSHOP_REGISTRATION_URL", "#")
    )


def _curriculum_sessions(workshop):
    sessions = OrderedDict()
    for module in workshop.curriculum_items.all():
        key = module.session_key
        if key not in sessions:
            sessions[key] = {
                "key": key,
                "label": module.session_label,
                "title": module.session_title,
                "day": module.session_day,
                "time": module.session_time,
                "modules": [],
            }
        sessions[key]["modules"].append(module)
    return list(sessions.values())


def _public_workshops():
    return Workshop.objects.filter(is_published=True).select_related("mentor").prefetch_related(*WORKSHOP_PREFETCHES)


def _workshop_context(workshop):
    today = timezone.localdate()
    public = Workshop.objects.filter(is_published=True)

    previous_workshop = (
        public.filter(start_date__lt=workshop.start_date)
        .order_by("-start_date")
        .first()
    )
    newest_public_workshop = public.order_by("-start_date").first()
    latest_workshop = (
        newest_public_workshop
        if newest_public_workshop is not None and newest_public_workshop.pk != workshop.pk
        else None
    )

    workshop.registration_link = _registration_url(workshop)
    workshop.recording_request_link = _recording_request_url()

    return {
        "workshop": workshop,
        "previous_workshop": previous_workshop,
        "latest_workshop": latest_workshop,
        "curriculum_sessions": _curriculum_sessions(workshop),
        "testimonials": Testimonial.objects.filter(is_active=True),
        "today": today,
    }


def home(request):
    today = timezone.localdate()
    workshop = (
        _public_workshops()
        .filter(is_archived=False, end_date__gte=today)
        .order_by("start_date")
        .first()
    )
    if workshop is None:
        workshop = _public_workshops().order_by("-start_date").first()
    if workshop is None:
        return render(request, "workshop/list.html", {"workshops": [], "today": today})
    return render(request, "workshop/detail.html", _workshop_context(workshop))


def workshop_detail(request, slug):
    workshop = get_object_or_404(_public_workshops(), slug=slug)
    return render(request, "workshop/detail.html", _workshop_context(workshop))


def workshop_list(request):
    workshops = _public_workshops().order_by("-start_date")
    return render(
        request,
        "workshop/list.html",
        {
            "workshops": workshops,
            "today": timezone.localdate(),
        },
    )
