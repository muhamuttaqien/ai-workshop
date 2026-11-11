from django.shortcuts import get_object_or_404, render

from .models import Course


def _public_courses():
    return Course.objects.filter(is_published=True)


def home(request):
    return render(
        request,
        "courses/home.html",
        {"featured_courses": _public_courses()[:5]},
    )


def course_list(request):
    return render(
        request,
        "courses/list.html",
        {"courses": _public_courses()},
    )


def course_detail(request, slug):
    course = get_object_or_404(_public_courses(), slug=slug)
    related_courses = _public_courses().exclude(pk=course.pk)[:3]
    return render(
        request,
        "courses/detail.html",
        {"course": course, "related_courses": related_courses},
    )
