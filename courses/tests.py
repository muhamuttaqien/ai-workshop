from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Course


class LearningPlatformTests(TestCase):
    def test_homepage_is_courses_platform(self):
        self.assertEqual(reverse("courses:home"), "/")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Belajar AI untuk")
        self.assertContains(response, "ChatGPT untuk Aktivitas Sehari-hari")
        self.assertContains(response, 'href="/workshop/"')

    def test_homepage_navigation_and_learning_journey(self):
        response = self.client.get(reverse("courses:home"))
        self.assertNotContains(response, "Jelajahi Courses")
        self.assertContains(response, 'aria-label="Navigasi Utama"')
        self.assertContains(response, 'href="/">Beranda</a>')
        self.assertContains(response, 'href="/courses/">Courses</a>')
        self.assertContains(response, 'href="/workshop/">Workshop</a>')
        self.assertContains(response, "Mulai Belajar AI Sekarang!")
        for phrase in (
            "Buat Akun Gratis",
            "Pelajari Materi Video",
            "Kerjakan Kuis",
            "Praktik Langsung",
            "masih dalam pengembangan",
        ):
            self.assertContains(response, phrase)
        html = response.content.decode("utf-8")
        self.assertLess(
            html.index("Courses untuk mulai belajar AI."),
            html.index("Mulai Belajar AI Sekarang!"),
        )
        self.assertLess(
            html.index("Mulai Belajar AI Sekarang!"),
            html.index("Ingin belajar bersama mentor?"),
        )

    def test_courses_catalog_and_details(self):
        response = self.client.get(reverse("courses:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Claude untuk Riset dan Menulis")
        course = Course.objects.get(slug="claude-untuk-riset-dan-menulis")
        detail = self.client.get(reverse("courses:detail", kwargs={"slug": course.slug}))
        self.assertContains(detail, course.description)
        self.assertContains(detail, "Segera Hadir")
        self.assertContains(detail, "Memahami fungsi AI sebagai pendamping riset")

    def test_unpublished_course_is_not_public(self):
        course = Course.objects.create(
            title="Hidden Demo Course",
            slug="hidden-course",
            short_description="Hidden course",
            description="Hidden description",
            is_published=False,
        )
        self.assertNotContains(self.client.get(reverse("courses:list")), course.title)
        self.assertEqual(
            self.client.get(reverse("courses:detail", args=[course.slug])).status_code,
            404,
        )

    def test_workshop_routes_are_preserved(self):
        self.assertEqual(reverse("workshop:home"), "/workshop/")
        self.assertEqual(reverse("workshop:list"), "/workshops/")
        self.assertEqual(
            reverse("workshop:detail", args=["claude-untuk-riset"]),
            "/workshop/claude-untuk-riset/",
        )
        response = self.client.get("/workshop/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "AI untuk Semua")
        self.assertEqual(self.client.get("/workshop").status_code, 302)
        self.assertEqual(
            self.client.get("/workshop").headers["Location"], "/workshop/"
        )

    def test_separate_admin_sites(self):
        user = get_user_model().objects.create_superuser(
            username="admin_courses_test", email="test@example.com", password="safe-demo-password-123"
        )
        self.client.force_login(user)
        courses_index = self.client.get("/admin-courses/")
        self.assertEqual(courses_index.status_code, 200)
        self.assertContains(courses_index, "Kelola Courses")
        self.assertContains(courses_index, "Courses")
        self.assertNotContains(courses_index, "Kelola Workshop")
        self.assertEqual(
            self.client.get(reverse("courses_admin:courses_course_changelist")).status_code,
            200,
        )
        workshop_index = self.client.get("/admin-workshop/")
        self.assertEqual(workshop_index.status_code, 200)
        self.assertContains(workshop_index, "Kelola Workshop")
        self.assertEqual(
            self.client.get(reverse("workshop_admin:workshop_workshop_changelist")).status_code,
            200,
        )
        self.assertEqual(self.client.get("/admin-courses/workshop/workshop/").status_code, 404)
        self.assertEqual(self.client.get("/admin-workshop/courses/course/").status_code, 404)
