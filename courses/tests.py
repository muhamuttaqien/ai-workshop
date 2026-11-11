from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Course, Lesson, QuizQuestion


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
                self.assertContains(response, 'class="brand-text">Indonesia AI (Courses)</span>')
                self.assertNotContains(response, "AI untuk Semua")
                self.assertContains(response, 'href="/courses/">Courses</a>')

        workshop_response = self.client.get("/workshop/")
        self.assertContains(workshop_response, 'aria-label="Indonesia AI (Workshop)"')
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

    def test_course_detail_has_three_ordered_sections(self):
        response = self.client.get(reverse("courses:detail", args=["chatgpt-untuk-aktivitas-sehari-hari"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "01 /")
        self.assertContains(response, "02 /")
        self.assertContains(response, "03 /")
        self.assertContains(response, "DAFTAR MATERI")
        self.assertContains(response, "LANJUTKAN EKSPLORASI")
        self.assertContains(response, "Mulai Belajar")
        html = response.content.decode()
        self.assertLess(html.index("TENTANG COURSE"), html.index("DAFTAR MATERI"))
        self.assertLess(html.index("DAFTAR MATERI"), html.index("LANJUTKAN EKSPLORASI"))
        self.assertContains(
            response,
            'href="/courses/chatgpt-untuk-aktivitas-sehari-hari/lessons/mengenal-chatgpt/"',
        )

    def test_seeded_lessons_and_quizzes_are_accessible(self):
        self.assertEqual(Lesson.objects.filter(is_published=True).count(), 15)
        self.assertEqual(QuizQuestion.objects.count(), 15)
        for course in Course.objects.filter(is_published=True):
            with self.subTest(course=course.slug):
                self.assertEqual(course.lessons.filter(is_published=True).count(), 3)
                first = course.lessons.first()
                response = self.client.get(reverse("courses:lesson", args=[course.slug, first.slug]))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, first.title)
                self.assertContains(response, 'aria-label="Daftar materi"')
                self.assertContains(response, "Video pembelajaran sedang disiapkan")
                self.assertContains(response, "PENJELASAN MATERI")
                self.assertContains(response, "KUIS PEMAHAMAN")
                self.assertContains(response, "Periksa Jawaban")
                self.assertContains(response, "Materi Berikutnya")
                self.assertContains(response, 'id="course-theme-toggle"')

    def test_mini_switch_and_header_alignment_styles(self):
        from pathlib import Path
        from django.contrib.staticfiles import finders

        theme_styles = Path(finders.find("courses/themes.css")).read_text(encoding="utf-8")
        main_styles = Path(finders.find("courses/style.css")).read_text(encoding="utf-8")
        self.assertIn("width: 56px;", theme_styles)
        self.assertIn("height: 36px;", theme_styles)
        self.assertIn("width: 26px;", theme_styles)
        self.assertIn("height: 26px;", theme_styles)
        self.assertIn("height: 76px;", main_styles)
        self.assertIn("height: 68px;", main_styles)
        self.assertIn("width: min(1160px, calc(100% - 48px))", main_styles)

    def test_home_ticker_removed_and_compact_theme_toggle(self):
        response = self.client.get(reverse("courses:home"))
        self.assertNotContains(response, "BUKAN CUMA TEORI")
        self.assertNotContains(response, "BELAJAR DENGAN CONTOH")
        self.assertNotContains(response, "COBA SENDIRI")
        self.assertNotContains(response, "platform-ticker")
        self.assertContains(response, 'id="course-theme-toggle"')
        self.assertNotContains(response, 'class="theme-label"')

    def test_floating_theme_control_and_scoped_course_brand(self):
        for route in (
            reverse("courses:home"),
            reverse("courses:list"),
            reverse("courses:detail", args=["notebooklm-untuk-belajar-dari-dokumen"]),
            reverse("courses:lesson", args=[
                "notebooklm-untuk-belajar-dari-dokumen", "mengenal-notebooklm",
            ]),
        ):
            response = self.client.get(route)
            self.assertContains(response, 'class="brand-text">Indonesia AI (Courses)</span>')
            self.assertContains(response, 'id="course-theme-toggle"', count=1)
            html = response.content.decode("utf-8")
            self.assertLess(html.index("</footer>"), html.index('id="course-theme-toggle"'))
            self.assertNotIn('class="theme-label"', html)

        lesson = self.client.get(reverse("courses:lesson", args=[
            "notebooklm-untuk-belajar-dari-dokumen", "mengenal-notebooklm",
        ]))
        self.assertNotContains(lesson, 'class="lesson-sidebar-back"')
        self.assertNotContains(lesson, "> Semua Materi</a>")
        self.assertContains(lesson, "Video pembelajaran sedang disiapkan")

    def test_workshop_brand_has_workshop_suffix_only(self):
        response = self.client.get(reverse("workshop:home"))
        self.assertContains(response, 'class="brand-text">Indonesia AI (Workshop)</span>')
        self.assertNotContains(response, 'id="course-theme-toggle"')
        self.assertNotContains(response, 'class="brand-text">Indonesia AI (Courses)</span>')

    def test_lesson_sidebar_has_three_lessons_without_play_arrow(self):
        for course in Course.objects.filter(is_published=True):
            lesson = course.lessons.filter(is_published=True).first()
            response = self.client.get(reverse("courses:lesson", args=[course.slug, lesson.slug]))
            self.assertContains(response, 'class="lesson-nav-item', count=3)
            self.assertNotContains(response, "fa-solid fa-play")
            self.assertContains(response, "MATERI 01 / 03")

    def test_quiz_grading_and_answer_feedback(self):
        course = Course.objects.get(slug="chatgpt-untuk-aktivitas-sehari-hari")
        lesson = course.lessons.get(slug="mengenal-chatgpt")
        question = lesson.quiz_questions.first()
        url = reverse("courses:lesson", args=[course.slug, lesson.slug])

        initial = self.client.get(url)
        self.assertNotContains(initial, "Hasil Kuis:")
        correct = self.client.post(url, {f"question_{question.pk}": question.correct_option})
        self.assertContains(correct, "Hasil Kuis: 1 / 1")
        self.assertContains(correct, "Benar")
        self.assertContains(correct, question.explanation)
        wrong_answer = next(option for option in "abcd" if option != question.correct_option)
        wrong = self.client.post(url, {f"question_{question.pk}": wrong_answer})
        self.assertContains(wrong, "Hasil Kuis: 0 / 1")
        self.assertContains(wrong, "Belum Tepat")

    def test_lesson_is_scoped_to_published_course_and_published_lesson(self):
        published = Course.objects.get(slug="chatgpt-untuk-aktivitas-sehari-hari")
        hidden = Course.objects.create(
            title="Draft Course", slug="draft-course", short_description="Draft",
            description="Draft", is_published=False,
        )
        draft_lesson = Lesson.objects.create(
            course=published, title="Hidden Lesson", slug="hidden-lesson",
            content="Draft", is_published=False,
        )
        foreign_lesson = Lesson.objects.create(
            course=hidden, title="Foreign Lesson", slug="foreign-lesson",
            content="Draft", is_published=True,
        )
        self.assertEqual(
            self.client.get(reverse("courses:lesson", args=[published.slug, draft_lesson.slug])).status_code,
            404,
        )
        self.assertEqual(
            self.client.get(reverse("courses:lesson", args=[hidden.slug, foreign_lesson.slug])).status_code,
            404,
        )
        self.assertEqual(
            self.client.get(reverse("courses:lesson", args=[published.slug, foreign_lesson.slug])).status_code,
            404,
        )

    def test_video_embed_accepts_youtube_id_only(self):
        lesson = Lesson.objects.get(
            course__slug="chatgpt-untuk-aktivitas-sehari-hari", slug="mengenal-chatgpt"
        )
        lesson.youtube_video_id = "dQw4w9WgXcQ"
        lesson.full_clean()
        lesson.save(update_fields=["youtube_video_id"])
        response = self.client.get(reverse("courses:lesson", args=[lesson.course.slug, lesson.slug]))
        self.assertContains(
            response, 'src="https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ"'
        )
        lesson.youtube_video_id = "https://example.com/?unsafe"
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            lesson.full_clean()

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
        self.assertEqual(
            self.client.get(reverse("courses_admin:courses_lesson_changelist")).status_code,
            200,
        )
        self.assertEqual(self.client.get("/admin-courses/workshop/workshop/").status_code, 404)
        self.assertEqual(self.client.get("/admin-workshop/courses/course/").status_code, 404)
