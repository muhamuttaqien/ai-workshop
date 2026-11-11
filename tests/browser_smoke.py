"""Browser smoke checks for all public Workshop AI layout variants.

Run after 'python manage.py migrate' and 'python -m playwright install chromium'.
"""
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.request import urlopen

from playwright.sync_api import sync_playwright


BASE_URL = "http://127.0.0.1:8765"
WORKSHOPS = [
    ("claude-untuk-riset", "editorial"),
    ("chatgpt-pendataan-harian", "workflow"),
    ("gemini-laporan-kerja", "dashboard"),
    ("canva-ai-konten-media-sosial", "showcase"),
    ("gamma-presentasi-profesional", "showcase"),
    ("notebooklm-belajar-dari-dokumen", "guide"),
]
SECTION_IDS = [
    "tentang", "untuk-siapa", "materi", "benefit", "jadwal",
    "mentor", "daftar", "testimonial", "faq",
]


def main():
    server = subprocess.Popen(
        [
            sys.executable, "manage.py", "runserver", "--noreload",
            "127.0.0.1:8765",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )
    try:
        for attempt in range(80):
            try:
                with urlopen(BASE_URL + "/workshops/", timeout=2) as response:
                    if response.status == 200:
                        break
            except (URLError, TimeoutError):
                time.sleep(.25)
        else:
            raise RuntimeError("Django development server did not start")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                for width in (1440, 390):
                    page = browser.new_page(
                        viewport={"width": width, "height": 850},
                        device_scale_factor=1,
                    )
                    try:
                        response = page.goto(BASE_URL + "/", wait_until="load")
                        assert response is not None and response.status == 200
                        assert page.locator(".platform-brand .brand-mark").count() == 2
                        assert page.locator(".platform-header .brand-text").inner_text() == "Indonesia AI"
                        assert page.locator(".platform-header .brand-mark").evaluate(
                            "(el) => getComputedStyle(el).backgroundColor"
                        ) == "rgb(239, 77, 77)", ("Courses logo background", width)
                        assert page.locator(".platform-nav-cta").count() == 0
                        assert page.locator(".hero-actions a").count() == 2
                        assert page.locator(".hero-actions a").first.inner_text().strip().startswith("Lihat Program")
                        assert page.locator(".hero-actions a").first.get_attribute("href") == "#courses"
                        assert page.locator(".hero-actions a").nth(1).inner_text().strip().startswith("Jelajahi Courses")
                        assert page.locator(".learning-journey-grid, .journey-step").count() == 0
                        assert page.locator(".learning-journey-layout").count() == 1
                        assert page.locator(".learning-path-step").count() == 4
                        assert page.locator(".learning-path").evaluate(
                            "(el) => window.getComputedStyle(el).listStyleType"
                        ) == "none"
                        assert page.evaluate(
                            "() => document.documentElement.scrollWidth <= window.innerWidth + 1"
                        ), ("homepage horizontal overflow", width)

                        # Courses must have a completely independent dark UI.
                        assert page.locator("body").evaluate(
                            "(el) => getComputedStyle(el).backgroundColor"
                        ) == "rgb(11, 11, 14)", ("homepage dark background", width)
                        assert page.locator(".platform-header").evaluate(
                            "(el) => getComputedStyle(el).backgroundColor"
                        ).startswith("rgba(11, 11, 14,"), ("dark navigation", width)
                        assert page.locator(".hero-actions .button-primary").evaluate(
                            "(el) => getComputedStyle(el).backgroundColor"
                        ) == "rgb(239, 77, 77)", ("primary action red", width)
                        assert page.locator(".hero-copy h1").evaluate(
                            "(el) => getComputedStyle(el).color"
                        ) == "rgb(247, 247, 248)", ("hero text white", width)
                        assert page.locator(".hero-studio").count() == 1
                        assert page.locator(".studio-label").inner_text() == "PRATINJAU KONSEP"
                        assert page.locator(".course-card").count() == 5
                        # In-page navigation should scroll to the first program section.
                        page.locator(".hero-actions a").first.click()
                        page.wait_for_function("() => window.location.hash === '#courses'")
                        page.wait_for_function(
                            "() => document.querySelector('#courses').getBoundingClientRect().top < 150"
                        )

                        # Switch to light mode and retain preference between Courses pages.
                        toggle = page.locator("#course-theme-toggle")
                        assert toggle.get_attribute("aria-label") == "Aktifkan mode terang"
                        toggle.click()
                        assert page.locator("html").get_attribute("data-theme") == "light"
                        assert toggle.get_attribute("aria-label") == "Aktifkan mode gelap"
                        assert page.locator("body").evaluate(
                            "(el) => getComputedStyle(el).backgroundColor"
                        ) == "rgb(255, 255, 255)", ("light homepage", width)
                        assert page.evaluate(
                            "() => localStorage.getItem('indonesia-ai-course-theme')"
                        ) == "light"

                        for route, selector in (
                            ("/courses/", ".catalog-layout"),
                            ("/courses/gemini-untuk-produktivitas-dan-laporan/", ".detail-content"),
                            ("/courses/notebooklm-untuk-belajar-dari-dokumen/", ".detail-content"),
                        ):
                            course_response = page.goto(BASE_URL + route, wait_until="load")
                            assert course_response is not None and course_response.status == 200, route
                            assert page.locator(selector).count() == 1, (route, selector)
                            assert page.locator("html").get_attribute("data-theme") == "light", route
                            assert page.locator("body").evaluate(
                                "(el) => getComputedStyle(el).backgroundColor"
                            ) == "rgb(255, 255, 255)", ("light course", route, width)
                            assert page.evaluate(
                                "() => document.documentElement.scrollWidth <= window.innerWidth + 1"
                            ), ("light course horizontal overflow", route, width)

                        # Return to dark mode; choice must persist across navigation.
                        page.locator("#course-theme-toggle").click()
                        assert page.locator("html").get_attribute("data-theme") is None
                        assert page.locator("#course-theme-toggle").get_attribute("aria-label") == "Aktifkan mode terang"
                        assert page.evaluate(
                            "() => localStorage.getItem('indonesia-ai-course-theme')"
                        ) == "dark"

                        for route, selector in (
                            ("/courses/", ".catalog-layout"),
                            ("/courses/chatgpt-untuk-aktivitas-sehari-hari/", ".detail-content"),
                        ):
                            course_response = page.goto(BASE_URL + route, wait_until="domcontentloaded")
                            assert course_response is not None and course_response.status == 200, route
                            assert page.locator(selector).count() == 1, (route, selector)
                            assert page.locator("html").get_attribute("data-theme") is None, route
                            assert page.locator("body").evaluate(
                                "(el) => getComputedStyle(el).backgroundColor"
                            ) == "rgb(11, 11, 14)", ("dark course page", route, width)
                            assert page.evaluate(
                                "() => document.documentElement.scrollWidth <= window.innerWidth + 1"
                            ), ("courses horizontal overflow", route, width)

                        # Course detail: ordered syllabus, lesson video/text/quiz and navigation.
                        detail_url = BASE_URL + "/courses/chatgpt-untuk-aktivitas-sehari-hari/"
                        detail_response = page.goto(detail_url, wait_until="load")
                        assert detail_response is not None and detail_response.status == 200
                        labels = page.locator(".detail-section .section-index, .course-syllabus-section .section-index, .related-section .section-index")
                        assert labels.all_inner_texts() == ["01 /", "02 /", "03 /"]
                        assert page.locator(".syllabus-list li").count() == 2
                        page.locator(".syllabus-start").click()
                        assert page.url.endswith("/courses/chatgpt-untuk-aktivitas-sehari-hari/lessons/mengenal-chatgpt/")
                        assert page.locator(".lesson-sidebar-nav a").count() == 2
                        assert page.locator(".lesson-nav-item.active").count() == 1
                        assert page.locator(".lesson-video-placeholder").count() == 1
                        assert page.locator(".lesson-content-text p").count() >= 2
                        assert page.locator(".quiz-question").count() == 1
                        page.locator(".quiz-option input[value='b']").check()
                        page.locator(".quiz-submit").click()
                        assert "Hasil Kuis: 1 / 1" in page.locator(".quiz-feedback h3").inner_text()
                        assert page.evaluate(
                            "() => document.documentElement.scrollWidth <= window.innerWidth + 1"
                        ), ("lesson horizontal overflow", width)
                        # The lesson pages use the same persisted light/dark preference.
                        page.locator("#course-theme-toggle").click()
                        assert page.locator("html").get_attribute("data-theme") == "light"
                        page.locator(".lesson-bottom-nav a").last.click()
                        assert page.url.endswith("/lessons/menulis-prompt-yang-jelas/")
                        assert page.locator("html").get_attribute("data-theme") == "light"
                        assert page.evaluate(
                            "() => document.documentElement.scrollWidth <= window.innerWidth + 1"
                        ), ("light lesson horizontal overflow", width)
                        page.locator("#course-theme-toggle").click()
                        assert page.locator("html").get_attribute("data-theme") is None

                        for slug, layout in WORKSHOPS:
                            url = BASE_URL + "/workshop/" + slug + "/"
                            response = page.goto(url, wait_until="domcontentloaded")
                            assert response is not None and response.status == 200, url
                            assert page.locator("body").get_attribute("class") == "layout-" + layout, url
                            assert page.locator(".site-header .brand-text").inner_text() == "Indonesia AI", url
                            assert page.locator("#course-theme-toggle").count() == 0, url
                            assert page.locator(".site-header .nav-links a").filter(has_text="Courses").count() == 0, url
                            assert page.locator(".hero h1").count() == 1, url
                            assert page.locator(".hero h1").inner_text().strip(), url
                            assert page.locator(".hero-subtitle").inner_text().strip(), url

                            for section_id in SECTION_IDS:
                                assert page.locator("section#" + section_id).count() == 1, (url, section_id)

                            for selector in (
                                ".workshop-outcome-card h3",
                                ".workshop-audience-card h3",
                                ".workshop-module h4",
                                ".workshop-benefit-card h3",
                                ".schedule-card h3",
                                ".mentor-card h3",
                                ".testimonial-card p",
                                ".faq-question",
                            ):
                                locator = page.locator(selector)
                                assert locator.count() > 0, (url, selector)
                                assert all(x.strip() for x in locator.all_inner_texts()), (url, selector)

                            assert page.locator(".workshop-card-number").first.inner_text().strip(), url
                            assert page.locator(".workshop-audience-icon").first.inner_text().strip(), url
                            assert page.locator(".workshop-module-number").first.inner_text().strip(), url
                            assert page.locator(".meta-icon i.fa-solid, .meta-icon i.fa-regular").count() == 3, url

                            color = page.locator(".hero h1").evaluate(
                                "(element) => window.getComputedStyle(element).color"
                            )
                            if layout in ("workflow", "showcase", "guide"):
                                assert color == "rgb(255, 255, 255)", (url, color)

                            mentor_card = page.locator(".mentor-card-interactive")
                            assert mentor_card.count() == 1, url
                            assert "Muhammad Angga Muttaqien, M.Eng." in mentor_card.inner_text(), url
                            assert "GRID Co., Ltd." in page.locator(".mentor-card-detail").inner_text(), url
                            assert page.locator(".mentor-more-btn, .mentor-back-btn").count() == 0, url

                            if width == 1440:
                                mentor_card.hover()
                                assert "is-expanded" in mentor_card.get_attribute("class"), url
                                assert page.locator(".mentor-card-detail").get_attribute("aria-hidden") == "false", url
                                page.wait_for_timeout(700)
                                card_bounds = mentor_card.bounding_box()
                                detail_bounds = page.locator(".mentor-card-detail").bounding_box()
                                assert abs(card_bounds["x"] - detail_bounds["x"]) < 5, (url, card_bounds, detail_bounds)
                                page.mouse.move(1, 1)
                                assert "is-expanded" not in mentor_card.get_attribute("class"), url
                            else:
                                track = page.locator(".mentor-card-track")
                                assert track.evaluate(
                                    "(element) => window.getComputedStyle(element).flexDirection"
                                ) == "column", url
                                assert page.locator(".mentor-card-detail").get_attribute("aria-hidden") == "false", url
                                assert page.locator(".mentor-card-detail").is_visible(), url

                            assert page.locator(".mentor-card-detail").evaluate(
                                "(element) => element.scrollHeight <= element.clientHeight + 3"
                            ), ("mentor biography overflow", url)

                            if width == 390:
                                assert page.locator(".mobile-cta").count() == 1, url
                                display = page.locator(".workshop-outcomes").evaluate(
                                    "(element) => window.getComputedStyle(element).display"
                                )
                                assert display == "flex", (url, display)
                                if page.locator(".mobile-cta-archive").count():
                                    button = page.locator(".mobile-latest-workshop-btn")
                                    assert button.inner_text().strip().startswith("Workshop Terbaru"), url
                                    right_edge = button.bounding_box()["x"] + button.bounding_box()["width"]
                                    assert width - right_edge < 35, (url, right_edge)
                                else:
                                    assert page.locator(".mobile-price-current").inner_text().strip(), url
                            print("PASS", layout, slug, width, flush=True)
                    finally:
                        page.close()
            finally:
                browser.close()
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait(timeout=5)


if __name__ == "__main__":
    main()
