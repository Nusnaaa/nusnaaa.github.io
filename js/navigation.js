(() => {
    "use strict";
    const navigation = document.getElementById("navigation");
    if (!navigation) return;
    const isProjectPage = window.location.pathname.includes("/projects/");
    const prefix = isProjectPage ? "../" : "";
    navigation.innerHTML = `
        <nav class="site-nav" aria-label="Main navigation">
            <a class="site-logo" href="${prefix}index.html">Linus Adzanku</a>
            <div class="nav-links">
                <a href="${prefix}index.html">Home</a>
                <a href="${prefix}projects.html">Projects</a>
                <a href="${prefix}cv.html">CV</a>
                <a href="https://github.com/Nusnaaa" target="_blank" rel="noopener noreferrer">GitHub</a>
                <a href="${prefix}index.html#contact">Contact</a>
            </div>
        </nav>`;

    // Supply a skip link on the owner-maintained UAS page without editing its HTML.
    const main = document.querySelector("main");
    if (main) {
        if (!main.id) main.id = "main-content";
        if (!main.hasAttribute("tabindex")) main.tabIndex = -1;
        if (!document.querySelector(".skip-link")) {
            const skip = document.createElement("a");
            skip.className = "skip-link";
            skip.href = `#${main.id}`;
            skip.textContent = "Skip to main content";
            document.body.prepend(skip);
        }
    }

    // Overview pages are intentionally short and do not need the report TOC.
    if (isProjectPage && !document.querySelector("[data-project-overview]")) {
        if (!document.querySelector("link[data-project-toc-styles]")) {
            const styles = document.createElement("link");
            styles.rel = "stylesheet";
            styles.href = `${prefix}css/project-toc.css`;
            styles.dataset.projectTocStyles = "";
            document.head.appendChild(styles);
        }
        if (!document.querySelector("script[data-project-toc-script]")) {
            const script = document.createElement("script");
            script.src = `${prefix}js/project-toc.js`;
            script.dataset.projectTocScript = "";
            document.body.appendChild(script);
        }
    }
})();
