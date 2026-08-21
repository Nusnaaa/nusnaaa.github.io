const navigation = document.getElementById("navigation");

if (navigation) {

    // Project pages sit one directory below the root.
    const isProjectPage =
        window.location.pathname.includes("/projects/");

    const prefix = isProjectPage ? "../" : "";

    navigation.innerHTML = `

        <nav class="site-nav">

            <a class="site-logo" href="${prefix}index.html">
                Linus Adzanku
            </a>

            <div class="nav-links">

                <a href="${prefix}projects.html">
                    Projects
                </a>

                <a href="${prefix}cv.html">
                    CV
                </a>

                <a
                    href="https://www.linkedin.com/in/linus-adzanku"
                    target="_blank"
                    rel="noopener noreferrer">
                    LinkedIn
                </a>

            </div>

        </nav>

    `;

    /*
       Project-page table of contents
       --------------------------------
       Only project pages load these two files. Root pages such as
       index.html, projects.html, about.html and cv.html never request
       them, so the feature remains completely project-specific.
    */
    if (isProjectPage) {

        if (!document.querySelector('link[data-project-toc-styles]')) {
            const tocStyles = document.createElement("link");

            tocStyles.rel = "stylesheet";
            tocStyles.href = `${prefix}css/project-toc.css`;
            tocStyles.dataset.projectTocStyles = "";

            document.head.appendChild(tocStyles);
        }

        if (!document.querySelector('script[data-project-toc-script]')) {
            const tocScript = document.createElement("script");

            tocScript.src = `${prefix}js/project-toc.js`;
            tocScript.dataset.projectTocScript = "";

            document.body.appendChild(tocScript);
        }
    }
}
