from django.contrib.admin import AdminSite

from courses.admin import CourseAdmin, LessonAdmin
from courses.models import Course, Lesson
from workshop.admin import MentorAdmin, TestimonialAdmin, WorkshopAdmin
from workshop.models import Mentor, Testimonial, Workshop


class CoursesAdminSite(AdminSite):
    site_header = "Indonesia AI — Courses"
    site_title = "Courses Admin"
    index_title = "Kelola Courses"


class WorkshopAdminSite(AdminSite):
    site_header = "Indonesia AI — Workshop"
    site_title = "Workshop Admin"
    index_title = "Kelola Workshop"


courses_admin_site = CoursesAdminSite(name="courses_admin")
courses_admin_site.register(Course, CourseAdmin)
courses_admin_site.register(Lesson, LessonAdmin)

workshop_admin_site = WorkshopAdminSite(name="workshop_admin")
workshop_admin_site.register(Workshop, WorkshopAdmin)
workshop_admin_site.register(Mentor, MentorAdmin)
workshop_admin_site.register(Testimonial, TestimonialAdmin)
