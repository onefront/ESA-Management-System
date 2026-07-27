document.addEventListener("DOMContentLoaded", () => {

    const menuToggle = document.getElementById("menuToggle");
    const sidebar = document.querySelector(".sidebar");
    const overlay = document.getElementById("sidebarOverlay");

    if (!menuToggle || !sidebar || !overlay) {
        return;
    }

    // =====================================
    // Restore desktop sidebar state
    // =====================================
    if (window.innerWidth > 992) {

        if (localStorage.getItem("memberSidebar") === "collapsed") {

            document.body.classList.add("sidebar-collapsed");

        }

    }

    // =====================================
    // Toggle Sidebar
    // =====================================
    menuToggle.addEventListener("click", () => {

        // Mobile
        if (window.innerWidth <= 992) {

            sidebar.classList.toggle("show");
            overlay.classList.toggle("show");

        }

        // Desktop
        else {

            document.body.classList.toggle("sidebar-collapsed");

            if (document.body.classList.contains("sidebar-collapsed")) {

                localStorage.setItem("memberSidebar", "collapsed");

            } else {

                localStorage.setItem("memberSidebar", "expanded");

            }

        }

    });

    // =====================================
    // Close Mobile Sidebar
    // =====================================
    overlay.addEventListener("click", () => {

        sidebar.classList.remove("show");
        overlay.classList.remove("show");

    });

});