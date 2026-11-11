from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from .models import Course, Lesson


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
    lessons = course.lessons.filter(is_published=True)
    return render(
        request,
        "courses/detail.html",
        {"course": course, "related_courses": related_courses, "lessons": lessons},
    )


@require_http_methods(["GET", "POST"])
def lesson_detail(request, slug, lesson_slug):
    course = get_object_or_404(_public_courses(), slug=slug)
    lesson = get_object_or_404(
        Lesson.objects.filter(course=course, is_published=True),
        slug=lesson_slug,
    )
    lessons = list(course.lessons.filter(is_published=True))
    questions = list(lesson.quiz_questions.all())
    quiz_results = None
    quiz_score = 0
    if request.method == "POST" and questions:
        quiz_results = []
        for question in questions:
            selected = request.POST.get(f"question_{question.pk}", "")
            is_correct = selected == question.correct_option
            quiz_score += int(is_correct)
            quiz_results.append({
                "question": question,
                "selected": selected,
                "is_correct": is_correct,
            })
    return render(request, "courses/lesson.html", {
        "course": course,
        "lesson": lesson,
        "lessons": lessons,
        "questions": questions,
        "quiz_results": quiz_results,
        "quiz_score": quiz_score,
        "quiz_total": len(questions),
    })
