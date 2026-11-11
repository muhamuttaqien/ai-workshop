document.addEventListener("DOMContentLoaded", () => {
  const menuToggle = document.querySelector(".menu-toggle");
  const navLinks = document.querySelector(".nav-links");

  if (menuToggle && navLinks) {
    menuToggle.addEventListener("click", () => {
      const isOpen = navLinks.classList.toggle("open");
      menuToggle.setAttribute("aria-expanded", String(isOpen));
    });

    navLinks.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        navLinks.classList.remove("open");
        menuToggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  document.querySelectorAll(".faq-question").forEach((button) => {
    button.addEventListener("click", () => {
      const item = button.closest(".faq-item");
      const isOpen = item.classList.contains("open");

      document.querySelectorAll(".faq-item.open").forEach((openItem) => {
        if (openItem !== item) {
          openItem.classList.remove("open");
          openItem.querySelector(".faq-question").setAttribute("aria-expanded", "false");
        }
      });

      item.classList.toggle("open", !isOpen);
      button.setAttribute("aria-expanded", String(!isOpen));
    });
  });

  const revealObserver = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 }
  );

  document.querySelectorAll(".reveal").forEach((el) => revealObserver.observe(el));

  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();

  // Registration URL is supplied by Django via WORKSHOP_REGISTRATION_URL.
  document.querySelectorAll(".js-register").forEach((button) => {
    button.addEventListener("click", (event) => {
      if (button.getAttribute("href") === "#") {
        event.preventDefault();
        alert("Link pendaftaran belum disetel. Atur WORKSHOP_REGISTRATION_URL pada environment Django.");
      }
    });
  });

  const testimonialSection = document.querySelector(".testimonial-section");
  if (testimonialSection) {
    const track = testimonialSection.querySelector(".testimonial-track");
    const cards = Array.from(testimonialSection.querySelectorAll(".testimonial-card"));
    const prevButton = testimonialSection.querySelector(".testimonial-prev");
    const nextButton = testimonialSection.querySelector(".testimonial-next");
    const progressBar = testimonialSection.querySelector(".testimonial-progress-bar");
    let testimonialIndex = 0;

    const getVisibleCount = () => {
      if (window.innerWidth <= 620) return 1;
      if (window.innerWidth <= 900) return 2;
      return 3;
    };

    const updateTestimonials = () => {
      const visibleCount = getVisibleCount();
      const maxIndex = Math.max(0, cards.length - visibleCount);
      testimonialIndex = Math.min(testimonialIndex, maxIndex);

      const firstCard = cards[0];
      if (!firstCard) return;

      const trackStyle = window.getComputedStyle(track);
      const gap = parseFloat(trackStyle.columnGap || trackStyle.gap || "0");
      const step = firstCard.getBoundingClientRect().width + gap;
      track.style.transform = `translateX(-${testimonialIndex * step}px)`;

      prevButton.disabled = testimonialIndex === 0;
      nextButton.disabled = testimonialIndex >= maxIndex;

      const progress = maxIndex === 0 ? 100 : ((testimonialIndex + 1) / (maxIndex + 1)) * 100;
      progressBar.style.width = `${progress}%`;
    };

    prevButton.addEventListener("click", () => {
      testimonialIndex = Math.max(0, testimonialIndex - 1);
      updateTestimonials();
    });

    nextButton.addEventListener("click", () => {
      const maxIndex = Math.max(0, cards.length - getVisibleCount());
      testimonialIndex = Math.min(maxIndex, testimonialIndex + 1);
      updateTestimonials();
    });

    let resizeTimer;
    window.addEventListener("resize", () => {
      window.clearTimeout(resizeTimer);
      resizeTimer = window.setTimeout(updateTestimonials, 120);
    });

    updateTestimonials();
  }


  // Mobile auto-slide for Outcome and Audience cards.
  const initMobileAutoCarousel = (selector) => {
    const container = document.querySelector(selector);
    if (!container) return;

    const cards = Array.from(container.children);
    if (cards.length < 2) return;

    const mobileQuery = window.matchMedia("(max-width: 760px)");
    const reducedMotionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");

    let timer = null;
    let resumeTimer = null;
    let isUserInteracting = false;

    const getGap = () => {
      const styles = window.getComputedStyle(container);
      return parseFloat(styles.columnGap || styles.gap || "0") || 0;
    };

    const getStep = () => {
      const firstCard = cards[0];
      if (!firstCard) return 0;
      return firstCard.getBoundingClientRect().width + getGap();
    };

    const getCurrentIndex = () => {
      const step = getStep();
      if (!step) return 0;
      return Math.max(
        0,
        Math.min(cards.length - 1, Math.round(container.scrollLeft / step))
      );
    };

    const goToIndex = (index, smooth = true) => {
      const target = cards[index];
      if (!target) return;

      container.scrollTo({
        left: target.offsetLeft - cards[0].offsetLeft,
        behavior: smooth && !reducedMotionQuery.matches ? "smooth" : "auto",
      });
    };

    const stop = () => {
      if (timer) {
        window.clearInterval(timer);
        timer = null;
      }
    };

    const start = () => {
      stop();

      if (
        !mobileQuery.matches ||
        reducedMotionQuery.matches ||
        document.hidden ||
        cards.length < 2
      ) {
        return;
      }

      timer = window.setInterval(() => {
        if (isUserInteracting) return;

        const current = getCurrentIndex();
        const next = current >= cards.length - 1 ? 0 : current + 1;
        goToIndex(next);
      }, 3800);
    };

    const pauseForInteraction = () => {
      isUserInteracting = true;
      stop();

      if (resumeTimer) window.clearTimeout(resumeTimer);
      resumeTimer = window.setTimeout(() => {
        isUserInteracting = false;
        start();
      }, 4500);
    };

    container.addEventListener("pointerdown", pauseForInteraction, { passive: true });
    container.addEventListener("touchstart", pauseForInteraction, { passive: true });
    container.addEventListener("wheel", pauseForInteraction, { passive: true });

    mobileQuery.addEventListener?.("change", () => {
      if (!mobileQuery.matches) goToIndex(0, false);
      start();
    });

    document.addEventListener("visibilitychange", start);
    window.addEventListener("resize", start);

    start();
  };

  initMobileAutoCarousel(".workshop-outcomes");
  initMobileAutoCarousel(".workshop-audience");

});
