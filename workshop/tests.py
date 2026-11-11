from datetime import date

from django.test import TestCase, override_settings
from django.urls import reverse

from .models import (
    Mentor,
    Workshop,
    WorkshopBenefit,
    WorkshopCurriculumModule,
    WorkshopFAQ,
)


class WorkshopPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        mentor = Mentor.objects.create(
            name="Mentor Test",
            role="AI Practitioner",
            bio="Bio mentor",
        )
        cls.previous = Workshop.objects.create(
            slug="workshop-lama",
            title="Workshop Lama",
            headline="Workshop",
            headline_accent="Lama",
            description="Workshop lama",
            layout_variant="workflow",
            start_date=date(2026, 10, 1),
            end_date=date(2026, 10, 2),
            dates_label="1 & 2 Oktober 2026",
            days_label="Kamis & Jumat",
            time_label="19.30–21.00 WIB",
            price_label="Rp390.000",
            intro_title="Intro",
            audience_title="Audience",
            curriculum_title="Curriculum",
            benefits_title="Benefits",
            schedule_title="Schedule",
            mentor=mentor,
            mentor_section_title="Mentor",
            is_archived=True,
            show_registration=False,
        )
        cls.current = Workshop.objects.create(
            slug="workshop-baru",
            title="Workshop Baru",
            headline="Workshop",
            headline_accent="Baru",
            description="Workshop baru",
            layout_variant="editorial",
            start_date=date(2099, 10, 15),
            end_date=date(2099, 10, 16),
            dates_label="15 & 16 Oktober 2099",
            days_label="Kamis & Jumat",
            time_label="19.30–21.00 WIB",
            price_label="Rp390.000",
            intro_title="Intro",
            audience_title="Audience",
            curriculum_title="Curriculum",
            benefits_title="Benefits",
            schedule_title="Schedule",
            mentor=mentor,
            mentor_section_title="Mentor",
        )
        WorkshopCurriculumModule.objects.create(
            workshop=cls.current,
            session_key="day-01",
            session_label="DAY 01",
            session_title="Sesi Pertama",
            session_day="Kamis",
            session_time="19.30–21.00 WIB",
            number="01",
            title="Materi Dinamis",
            text="Konten materi dari model terkait.",
            sort_order=1,
        )
        WorkshopBenefit.objects.create(
            workshop=cls.current,
            number="01",
            kicker="LIVE",
            title="Benefit Dinamis",
            text="Benefit dari database.",
            visual="live",
            sort_order=1,
        )
        WorkshopFAQ.objects.create(
            workshop=cls.current,
            question="FAQ Dinamis?",
            answer="Ya, dari database.",
            sort_order=1,
        )

    def test_dynamic_detail_route(self):
        response = self.client.get(reverse("workshop:detail", args=[self.previous.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Workshop Lama")

    def test_home_uses_next_non_archived_workshop(self):
        response = self.client.get(reverse("workshop:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Workshop Baru")

    def test_related_content_is_rendered(self):
        response = self.client.get(reverse("workshop:detail", args=[self.current.slug]))
        self.assertContains(response, "Materi Dinamis")
        self.assertContains(response, "Benefit Dinamis")
        self.assertContains(response, "FAQ Dinamis?")

    def test_unpublished_workshop_is_not_public(self):
        hidden = Workshop.objects.create(
            slug="draft-workshop",
            title="Draft Workshop",
            headline="Draft",
            headline_accent="Workshop",
            description="Draft",
            start_date=date(2099, 11, 1),
            end_date=date(2099, 11, 2),
            dates_label="1 & 2 November 2099",
            days_label="Senin & Selasa",
            time_label="19.30–21.00 WIB",
            intro_title="Intro",
            audience_title="Audience",
            curriculum_title="Curriculum",
            benefits_title="Benefits",
            schedule_title="Schedule",
            mentor=self.current.mentor,
            mentor_section_title="Mentor",
            is_published=False,
        )
        response = self.client.get(reverse("workshop:detail", args=[hidden.slug]))
        self.assertEqual(response.status_code, 404)

    def test_archive_page_lists_both(self):
        response = self.client.get(reverse("workshop:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Workshop Lama")
        self.assertContains(response, "Workshop Baru")

    def test_archived_page_latest_link_points_to_newest_published_workshop(self):
        middle = Workshop.objects.create(
            slug="workshop-tengah",
            title="Workshop Tengah",
            headline="Workshop",
            headline_accent="Tengah",
            description="Workshop tengah",
            start_date=date(2098, 1, 10),
            end_date=date(2098, 1, 11),
            dates_label="10 & 11 Januari 2098",
            days_label="Kamis & Jumat",
            time_label="19.30–21.00 WIB",
            intro_title="Intro",
            audience_title="Audience",
            curriculum_title="Curriculum",
            benefits_title="Benefits",
            schedule_title="Schedule",
            mentor=self.current.mentor,
            mentor_section_title="Mentor",
            is_archived=True,
            show_registration=False,
        )
        response = self.client.get(reverse("workshop:detail", args=[self.previous.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lihat workshop terbaru")
        self.assertContains(response, reverse("workshop:detail", args=[self.current.slug]))
        self.assertNotContains(response, f'href="{reverse("workshop:detail", args=[middle.slug])}">Lihat workshop terbaru')

    def test_workshop_default_format_is_zoom_online(self):
        self.assertEqual(self.current.format_label, "Zoom Online")


    def test_dashboard_layout_renders_distinct_variant(self):
        reporting = Workshop.objects.create(
            slug="gemini-reporting-test",
            title="Gemini Reporting",
            headline="Pakai Gemini",
            headline_accent="untuk Laporan",
            description="Workshop reporting",
            layout_variant="dashboard",
            start_date=date(2026, 9, 17),
            end_date=date(2026, 9, 18),
            dates_label="17 & 18 September 2026",
            days_label="Kamis & Jumat",
            time_label="19.30–21.00 WIB",
            price_label="Rp390.000",
            intro_title="Intro",
            audience_title="Audience",
            curriculum_title="Curriculum",
            benefits_title="Benefits",
            schedule_title="Schedule",
            mentor=self.current.mentor,
            mentor_section_title="Mentor",
            is_archived=True,
            show_registration=False,
        )
        response = self.client.get(reverse("workshop:detail", args=[reporting.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="hero hero-reporting"')
        self.assertContains(response, "reporting-hero-visual")

    @override_settings(WORKSHOP_RECORDING_REQUEST_URL="https://example.com/request-rekaman")
    def test_recording_cta_uses_polished_button_class(self):
        response = self.client.get(reverse("workshop:detail", args=[self.previous.slug]))
        self.assertContains(response, "btn-recording")
        self.assertContains(response, "fa-circle-play")

    @override_settings(WORKSHOP_RECORDING_REQUEST_URL="https://example.com/request-rekaman")
    def test_archived_workshop_has_recording_request_cta(self):
        response = self.client.get(reverse("workshop:detail", args=[self.previous.slug]))
        self.assertContains(response, "Request Beli Rekaman")
        self.assertContains(response, 'href="https://example.com/request-rekaman"')

    def test_active_workshop_shows_discounted_price_offer(self):
        response = self.client.get(reverse("workshop:detail", args=[self.current.slug]))
        self.assertContains(response, "Rp780.000")
        self.assertContains(response, "Rp390.000")
        self.assertContains(response, "50% OFF")

    def test_active_workshop_shows_combined_duration(self):
        self.current.duration_label = "2 Hari • Total 3 Jam (Live) + 6 Jam (Online)"
        self.current.save(update_fields=["duration_label"])
        response = self.client.get(reverse("workshop:detail", args=[self.current.slug]))
        self.assertContains(response, "2 Hari • Total 3 Jam (Live) + 6 Jam (Online)")

    def test_laptop_specification_faq_is_always_visible(self):
        response = self.client.get(reverse("workshop:detail", args=[self.current.slug]))
        self.assertContains(response, "Apakah ada spesifikasi laptop tertentu yang dibutuhkan?")
        self.assertContains(response, "laptop standar yang biasa digunakan untuk aktivitas sehari-hari")

    def test_editorial_layout_without_hero_image_uses_fallback(self):
        self.current.hero_image = ""
        self.current.save(update_fields=["hero_image"])
        response = self.client.get(reverse("workshop:detail", args=[self.current.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "hero-photo-card-fallback")
        self.assertContains(response, "fa-magnifying-glass-chart")
        self.assertNotContains(response, 'class="hero-photo"')



    def test_general_layout_choices_are_available(self):
        values = {value for value, _label in Workshop.LAYOUT_CHOICES}
        self.assertEqual(values, {"editorial", "workflow", "dashboard", "showcase", "guide"})

    def test_showcase_layout_renders_distinct_variant(self):
        self.current.layout_variant = "showcase"
        self.current.save(update_fields=["layout_variant"])
        response = self.client.get(reverse("workshop:detail", args=[self.current.slug]))
        self.assertContains(response, "hero-showcase")
        self.assertContains(response, "showcase-hero-visual")

    def test_guide_layout_renders_distinct_variant(self):
        self.current.layout_variant = "guide"
        self.current.save(update_fields=["layout_variant"])
        response = self.client.get(reverse("workshop:detail", args=[self.current.slug]))
        self.assertContains(response, "hero-guide")
        self.assertContains(response, "guide-hero-visual")
