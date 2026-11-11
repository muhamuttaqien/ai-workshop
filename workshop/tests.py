from datetime import date

from django.test import TestCase, override_settings
from django.urls import reverse

from .models import (
    Mentor,
    Workshop,
    WorkshopBenefit,
    WorkshopCurriculumModule,
    WorkshopFAQ,
    WorkshopOutcome,
    WorkshopAudience,
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
        Workshop.objects.exclude(
            pk__in=[self.previous.pk, self.current.pk]
        ).update(is_archived=True)
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
        self.assertContains(response, "hero-dashboard")
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


    def test_date_ended_workshop_header_links_to_all_workshops(self):
        ended = Workshop.objects.create(
            slug="ended-by-date",
            title="Ended by Date",
            headline="Ended",
            headline_accent="Workshop",
            description="Workshop ended by date",
            layout_variant="editorial",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 2),
            dates_label="1 & 2 Januari 2026",
            days_label="Kamis & Jumat",
            time_label="19.30–21.00 WIB",
            intro_title="Intro",
            audience_title="Audience",
            curriculum_title="Curriculum",
            benefits_title="Benefits",
            schedule_title="Schedule",
            mentor=self.current.mentor,
            mentor_section_title="Mentor",
            is_archived=False,
            show_registration=True,
        )
        response = self.client.get(reverse("workshop:detail", args=[ended.slug]))
        self.assertContains(response, "Semua Workshop")
        self.assertContains(response, reverse("workshop:list"))
        self.assertNotContains(response, ">Daftar Sekarang</a>")


    def test_seeded_showcase_and_guide_workshops_exist(self):
        expected = {
            "canva-ai-konten-media-sosial": "showcase",
            "gamma-presentasi-profesional": "showcase",
            "notebooklm-belajar-dari-dokumen": "guide",
        }
        for slug, layout in expected.items():
            workshop = Workshop.objects.get(slug=slug)
            self.assertEqual(workshop.layout_variant, layout)
            self.assertTrue(workshop.is_published)


    def test_all_layouts_share_the_same_sections(self):
        section_ids = [
            'id="tentang"',
            'id="untuk-siapa"',
            'id="materi"',
            'id="benefit"',
            'id="jadwal"',
            'id="mentor"',
            'id="daftar"',
            'id="testimonial"',
            'id="faq"',
        ]
        for layout in ["editorial", "workflow", "dashboard", "showcase", "guide"]:
            with self.subTest(layout=layout):
                self.current.layout_variant = layout
                self.current.save(update_fields=["layout_variant"])
                response = self.client.get(reverse("workshop:detail", args=[self.current.slug]))
                self.assertEqual(response.status_code, 200)
                html = response.content.decode("utf-8")
                self.assertIn("layout-" + layout, html)
                positions = []
                for section_id in section_ids:
                    self.assertEqual(html.count(section_id), 1, section_id)
                    positions.append(html.index(section_id))
                self.assertEqual(positions, sorted(positions))


    def test_all_layouts_render_card_numbers_and_icons(self):
        WorkshopOutcome.objects.create(
            workshop=self.current,
            number="01",
            title="Outcome untuk Audit",
            text="Deskripsi outcome.",
        )
        WorkshopAudience.objects.create(
            workshop=self.current,
            icon="",
            label="Audience untuk Audit",
            text="Deskripsi audience.",
        )
        for layout in ["editorial", "workflow", "dashboard", "showcase", "guide"]:
            with self.subTest(layout=layout):
                self.current.layout_variant = layout
                self.current.save(update_fields=["layout_variant"])
                response = self.client.get(reverse("workshop:detail", args=[self.current.slug]))
                html = response.content.decode("utf-8")
                self.assertIn('class="workshop-card-number">01</div>', html)
                self.assertIn('class="workshop-audience-icon">01</span>', html)
                self.assertIn('class="workshop-module-number">01</span>', html)
                self.assertContains(response, "Outcome untuk Audit")
                self.assertContains(response, "Audience untuk Audit")
                self.assertContains(response, "Materi Dinamis")

    def test_branding_and_ended_footer_cta_are_consistent(self):
        response = self.client.get(reverse("workshop:detail", args=[self.previous.slug]))
        self.assertContains(response, 'aria-label="Workshop AI"')
        self.assertContains(response, "Workshop AI • by Indonesia AI")
        self.assertNotContains(response, ">Daftar Workshop <i")


    def test_mentor_profile_data_and_degree_are_updated(self):
        mentor = Mentor.objects.get(name="Muhammad Angga Muttaqien, M.Eng.")
        self.assertIn("lebih dari 10 tahun", mentor.full_bio)
        self.assertIn("GRID Co., Ltd.", mentor.full_bio)
        self.assertIn("Advanced Industrial Science and Technology", mentor.full_bio)
        self.assertIn("Embodied AI", mentor.full_bio)
        self.assertIn("Human-Robot Interaction", mentor.full_bio)

    def test_mentor_slider_is_shared_across_all_five_layouts(self):
        mentor = Mentor.objects.get(name="Muhammad Angga Muttaqien, M.Eng.")
        self.current.mentor = mentor
        for layout in ["editorial", "workflow", "dashboard", "showcase", "guide"]:
            with self.subTest(layout=layout):
                self.current.layout_variant = layout
                self.current.save(update_fields=["mentor", "layout_variant"])
                response = self.client.get(reverse("workshop:detail", args=[self.current.slug]))
                self.assertContains(response, "Muhammad Angga Muttaqien, M.Eng.")
                self.assertContains(response, "mentor-card-track")
                self.assertNotContains(response, "mentor-more-btn")
                self.assertNotContains(response, "mentor-back-btn")
                self.assertContains(response, "mentor-card-detail")
                self.assertContains(response, "Kak Angga memiliki pengalaman lebih dari 10 tahun")

    def test_mentor_without_full_bio_keeps_simple_card(self):
        response = self.client.get(reverse("workshop:detail", args=[self.current.slug]))
        self.assertContains(response, "mentor-card-front")
        self.assertNotContains(response, "mentor-card-track")
        self.assertNotContains(response, "mentor-more-btn")
