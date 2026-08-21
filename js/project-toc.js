(() => {
    "use strict";

    /*
       Project Table of Contents
       -------------------------
       This script is deliberately defensive: even if it is included
       accidentally elsewhere, it will only initialise inside /projects/.
    */
    if (!window.location.pathname.includes("/projects/")) {
        return;
    }

    const contentRoot = document.querySelector("main") || document.body;

    if (document.querySelector(".project-toc")) {
        return;
    }

    document.documentElement.classList.add("project-toc-enabled");

    const headingSelector = "h2, h3, h4";

    const headings = Array.from(contentRoot.querySelectorAll(headingSelector))
        .filter((heading) => {
            if (heading.closest(".project-footer")) {
                return false;
            }

            if (heading.matches("[data-toc-exclude], .project-toc-ignore")) {
                return false;
            }

            if (heading.closest("[data-toc-exclude], .project-toc-ignore")) {
                return false;
            }

            return heading.textContent.trim().length > 0;
        });

    /*
       Very short placeholder project pages do not need a floating
       navigation control. Once a project has at least two meaningful
       sections, the TOC appears automatically.
    */
    if (headings.length < 2) {
        return;
    }

    const usedIds = new Set(
        Array.from(document.querySelectorAll("[id]"))
            .map((element) => element.id)
            .filter(Boolean)
    );

    const slugify = (text) => {
        const base = text
            .normalize("NFKD")
            .replace(/[\u0300-\u036f]/g, "")
            .toLowerCase()
            .replace(/&/g, " and ")
            .replace(/[^a-z0-9]+/g, "-")
            .replace(/^-+|-+$/g, "");

        return base || "section";
    };

    const ensureUniqueId = (heading, index) => {
        if (heading.id) {
            return heading.id;
        }

        const base = slugify(heading.textContent.trim());
        let candidate = base;
        let suffix = 2;

        while (usedIds.has(candidate)) {
            candidate = `${base}-${suffix}`;
            suffix += 1;
        }

        if (!candidate) {
            candidate = `section-${index + 1}`;
        }

        heading.id = candidate;
        usedIds.add(candidate);

        return candidate;
    };

    headings.forEach(ensureUniqueId);

    const toc = document.createElement("aside");
    toc.className = "project-toc";
    toc.setAttribute("aria-label", "On this page");

    toc.innerHTML = `
        <button
            class="project-toc__toggle"
            type="button"
            aria-expanded="false"
            aria-controls="project-toc-panel">
            <span class="project-toc__toggle-label">Contents</span>
            <span class="project-toc__toggle-icon" aria-hidden="true">
                ☰
            </span>
        </button>

        <div class="project-toc__backdrop" aria-hidden="true"></div>

        <div
            class="project-toc__panel"
            id="project-toc-panel"
            tabindex="-1">

            <div class="project-toc__header">
                <p class="project-toc__eyebrow">On this page</p>

                <button
                    class="project-toc__close"
                    type="button"
                    aria-label="Close table of contents">
                    ×
                </button>
            </div>

            <nav class="project-toc__nav" aria-label="Project sections">
                <ol class="project-toc__list"></ol>
            </nav>
        </div>
    `;

    document.body.appendChild(toc);

    const list = toc.querySelector(".project-toc__list");
    const toggle = toc.querySelector(".project-toc__toggle");
    const panel = toc.querySelector(".project-toc__panel");
    const closeButton = toc.querySelector(".project-toc__close");
    const backdrop = toc.querySelector(".project-toc__backdrop");

    const minimumLevel = Math.min(
        ...headings.map((heading) => Number(heading.tagName.slice(1)))
    );

    const links = headings.map((heading) => {
        const level = Number(heading.tagName.slice(1));
        const depth = Math.max(0, level - minimumLevel);

        const item = document.createElement("li");
        item.className = "project-toc__item";
        item.dataset.depth = String(depth);

        const link = document.createElement("a");
        link.className = "project-toc__link";
        link.href = `#${heading.id}`;
        link.dataset.targetId = heading.id;
        link.textContent = heading.textContent.trim();

        item.appendChild(link);
        list.appendChild(item);

        return link;
    });

    const isDrawerMode = () =>
        window.matchMedia("(max-width: 1580px)").matches;

    const openToc = () => {
        toc.classList.add("is-open");
        toggle.setAttribute("aria-expanded", "true");

        if (isDrawerMode()) {
            requestAnimationFrame(() => panel.focus());
        }
    };

    const closeToc = ({ restoreFocus = false } = {}) => {
        toc.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");

        if (restoreFocus) {
            toggle.focus();
        }
    };

    toggle.addEventListener("click", () => {
        if (toc.classList.contains("is-open")) {
            closeToc();
        } else {
            openToc();
        }
    });

    closeButton.addEventListener("click", () => {
        closeToc({ restoreFocus: true });
    });

    backdrop.addEventListener("click", () => {
        closeToc({ restoreFocus: true });
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && toc.classList.contains("is-open")) {
            closeToc({ restoreFocus: true });
        }
    });

    const reduceMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    );

    links.forEach((link) => {
        link.addEventListener("click", (event) => {
            const id = link.dataset.targetId;
            const target = document.getElementById(id);

            if (!target) {
                return;
            }

            event.preventDefault();

            target.scrollIntoView({
                behavior: reduceMotion.matches ? "auto" : "smooth",
                block: "start"
            });

            try {
                history.pushState(null, "", `#${encodeURIComponent(id)}`);
            } catch (error) {
                // The page still scrolls correctly if history is unavailable.
            }

            if (isDrawerMode()) {
                closeToc();
            }
        });
    });

    let activeId = null;
    let scrollFrame = null;

    const setActiveLink = (id) => {
        if (!id || id === activeId) {
            return;
        }

        activeId = id;

        links.forEach((link) => {
            const isActive = link.dataset.targetId === id;

            link.classList.toggle("is-active", isActive);

            if (isActive) {
                link.setAttribute("aria-current", "location");

                const item = link.closest(".project-toc__item");

                if (item && !isDrawerMode()) {
                    item.scrollIntoView({
                        block: "nearest",
                        inline: "nearest"
                    });
                }
            } else {
                link.removeAttribute("aria-current");
            }
        });
    };

    const updateActiveSection = () => {
        scrollFrame = null;

        const activationLine = Math.min(
            180,
            Math.max(96, window.innerHeight * 0.18)
        );

        let current = headings[0];

        for (const heading of headings) {
            const top = heading.getBoundingClientRect().top;

            if (top <= activationLine) {
                current = heading;
            } else {
                break;
            }
        }

        const nearBottom =
            window.innerHeight + window.scrollY >=
            document.documentElement.scrollHeight - 8;

        if (nearBottom) {
            current = headings[headings.length - 1];
        }

        setActiveLink(current.id);
    };

    const scheduleActiveUpdate = () => {
        if (scrollFrame !== null) {
            return;
        }

        scrollFrame = requestAnimationFrame(updateActiveSection);
    };

    window.addEventListener("scroll", scheduleActiveUpdate, {
        passive: true
    });

    window.addEventListener("resize", () => {
        if (!isDrawerMode()) {
            closeToc();
        }

        scheduleActiveUpdate();
    });

    /*
       If a page is opened with an existing hash, respect it. IDs already
       present in the HTML are preserved; generated IDs are only added to
       headings that did not have one.
    */
    if (window.location.hash) {
        const hashId = decodeURIComponent(window.location.hash.slice(1));
        const hashTarget = document.getElementById(hashId);

        if (hashTarget && headings.includes(hashTarget)) {
            setActiveLink(hashId);
        } else {
            updateActiveSection();
        }
    } else {
        updateActiveSection();
    }
})();
