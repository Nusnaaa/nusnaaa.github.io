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
}