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
        self.assertContains(response, "Jelajahi Courses", count=1)
        self.assertContains(response, 'href="#courses">Lihat Program')
        html = response.content.decode("utf-8")
        self.assertLess(html.index('href="#courses">Lihat Program'), html.index(">Jelajahi Courses"))
        self.assertNotContains(response, "platform-nav-cta")
        self.assertContains(response, 'class="learning-path"')
        self.assertNotContains(response, "learning-journey-grid")
        self.assertNotContains(response, "journey-step")
        self.assertContains(response, 'aria-label="Navigasi Utama"')
        self.assertContains(response, 'href="/">Beranda</a>')
        self.assertContains(response, 'href="/courses/">Courses</a>')
        self.assertContains(response, 'href="/workshop/">Workshop</a>')
        self.assertContains(response, "Mulai Belajar AI Sekarang!")
        for phrase in (
            "Buat Akun Gratis",
            "Akses Materi Video",
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

    def test_consistent_indonesia_ai_branding_and_workshop_navigation(self):
        for url in ("/", "/courses/", "/courses/chatgpt-untuk-aktivitas-sehari-hari/"):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertContains(response, 'class="brand-mark"')
                self.assertContains(response, 'class="brand-text">Indonesia AI</span>')
                self.assertNotContains(response, "AI untuk Semua")
                self.assertContains(response, 'href="/courses/">Courses</a>')

        workshop_response = self.client.get("/workshop/")
        self.assertContains(workshop_response, 'aria-label="Indonesia AI"')
        self.assertContains(workshop_response, '<span class="brand-mark">AI</span>')
        self.assertNotContains(workshop_response, 'href="/courses/">Courses</a>')
        self.assertContains(workshop_response, 'href="/workshop/">Workshop</a>')

    def test_courses_theme_uses_brand_palette(self):
        from pathlib import Path
        from django.contrib.staticfiles import finders

        stylesheet = finders.find("courses/style.css")
        self.assertIsNotNone(stylesheet)
        css = Path(stylesheet).read_text(encoding="utf-8")
        self.assertIn("--accent: #ef4d4d;", css)
        self.assertIn("--ink: #f7f7f8;", css)
        self.assertIn("--bg: #0b0b0e;", css)
        for obsolete_color in ("#70e5d5", "#a898ff", "var(--violet)"):
            self.assertNotIn(obsolete_color, css)

    def test_five_published_example_courses(self):
        self.assertEqual(Course.objects.filter(is_published=True).count(), 5)
        for slug, title in (
            ("gemini-untuk-produktivitas-dan-laporan", "Gemini untuk Produktivitas dan Laporan"),
            ("notebooklm-untuk-belajar-dari-dokumen", "NotebookLM untuk Belajar dari Dokumen"),
        ):
            with self.subTest(slug=slug):
                course = Course.objects.get(slug=slug)
                self.assertTrue(course.is_published)
                self.assertEqual(course.status, "coming_soon")
                self.assertEqual(course.title, title)
                self.assertContains(self.client.get(reverse("courses:list")), title)
                self.assertContains(
                    self.client.get(reverse("courses:detail", args=[slug])), title
                )
                self.assertContains(self.client.get(reverse("courses:home")), title)

    def test_course_theme_toggle_is_on_course_pages_only(self):
        for route in ("/", "/courses/", "/courses/gemini-untuk-produktivitas-dan-laporan/"):
            with self.subTest(route=route):
                response = self.client.get(route)
                self.assertContains(response, 'id="course-theme-toggle"')
                self.assertContains(response, "courses/themes.css")
                self.assertContains(response, "courses/theme.js")
                self.assertContains(response, "Aktifkan mode terang")
        self.assertNotContains(self.client.get("/workshop/"), 'id="course-theme-toggle"')

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
        self.assertContains(response, "Indonesia AI")
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
