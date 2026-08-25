(function () {
  const theme = localStorage.getItem("lld-theme") === "dark" ? "dark" : "light";
  document.documentElement.dataset.theme = theme;
})();

document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("themeBtn");
  if (btn) {
    btn.addEventListener("click", () => {
      const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
      document.documentElement.dataset.theme = next;
      localStorage.setItem("lld-theme", next);
    });
  }

  const tabs = [...document.querySelectorAll("[data-tab]")];
  const panels = [...document.querySelectorAll("[data-panel]")];
  function show(id) {
    tabs.forEach((t) => t.classList.toggle("active", t.dataset.tab === id));
    panels.forEach((p) => p.classList.toggle("active", p.dataset.panel === id));
  }
  tabs.forEach((t) => t.addEventListener("click", () => {
    show(t.dataset.tab);
    history.replaceState(null, "", "#" + t.dataset.tab);
  }));
  const initial = (location.hash || "").replace("#", "");
  if (initial && tabs.some((t) => t.dataset.tab === initial)) show(initial);
  else if (tabs[0]) show(tabs[0].dataset.tab);
});
