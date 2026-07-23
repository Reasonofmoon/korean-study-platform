(() => {
  document.querySelectorAll("[data-filter-root]").forEach((root) => {
    const buttons = [...root.querySelectorAll("[data-filter]")];
    const lessons = [...root.querySelectorAll("[data-lesson]")];
    const empty = root.querySelector("[data-empty]");

    buttons.forEach((button) => {
      button.addEventListener("click", () => {
        const selected = button.dataset.filter;
        let visible = 0;
        buttons.forEach((item) => {
          const active = item === button;
          item.classList.toggle("is-active", active);
          item.setAttribute("aria-pressed", String(active));
        });
        lessons.forEach((lesson) => {
          const matches = selected === "all" || lesson.dataset.subject === selected;
          lesson.hidden = !matches;
          if (matches) visible += 1;
        });
        if (empty) empty.hidden = visible !== 0;
      });
    });
  });
})();
