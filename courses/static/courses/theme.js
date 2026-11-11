// Courses only: persisted light/dark appearance, independent of Workshop.
(() => {
  "use strict";
  const button = document.getElementById("course-theme-toggle");
  if (!button) return;

  const key = "indonesia-ai-course-theme";
  const root = document.documentElement;
  const label = button.querySelector(".theme-label");
  const icon = button.querySelector(".theme-icon");
  const meta = document.querySelector('meta[name="theme-color"]');

  function setTheme(light) {
    if (light) {
      root.setAttribute("data-theme", "light");
    } else {
      root.removeAttribute("data-theme");
    }
    button.setAttribute("aria-pressed", String(light));
    button.setAttribute("aria-label", light ? "Aktifkan mode gelap" : "Aktifkan mode terang");
    if (label) label.textContent = light ? "Gelap" : "Terang";
    if (icon) icon.className = "fa-solid theme-icon " + (light ? "fa-moon" : "fa-sun");
    if (meta) meta.setAttribute("content", light ? "#ffffff" : "#0b0b0e");
  }

  // The small inline script in <head> has already restored any preference.
  setTheme(root.getAttribute("data-theme") === "light");

  button.addEventListener("click", () => {
    const light = root.getAttribute("data-theme") !== "light";
    setTheme(light);
    try { localStorage.setItem(key, light ? "light" : "dark"); }
    catch (e) { /* Theme still works when storage is unavailable. */ }
  });
})();
