document.addEventListener("DOMContentLoaded", function () {

    const header = document.getElementById("siteHeader");

    const menuToggle =
        document.getElementById("menuToggle");

    const menuClose =
        document.getElementById("menuClose");

    const navigationMenu =
        document.getElementById("navigationMenu");

    const navigationLinks =
        document.querySelectorAll(
            ".navbar-links a"
        );


    /* ========================================
       SCROLL EFFECT
    ======================================== */

    window.addEventListener("scroll", function () {

        if (window.scrollY > 50) {

            header.classList.add("scrolled");

        } else {

            header.classList.remove("scrolled");

        }

    });


    /* ========================================
       OPEN MOBILE MENU
    ======================================== */

    if (menuToggle) {

        menuToggle.addEventListener(
            "click",
            function () {

                navigationMenu.classList.add(
                    "active"
                );

                document.body.style.overflow =
                    "hidden";

            }
        );

    }


    /* ========================================
       CLOSE MOBILE MENU
    ======================================== */

    if (menuClose) {

        menuClose.addEventListener(
            "click",
            function () {

                navigationMenu.classList.remove(
                    "active"
                );

                document.body.style.overflow =
                    "";

            }
        );

    }


    /* ========================================
       CLOSE AFTER CLICKING LINK
    ======================================== */

    navigationLinks.forEach(
        function (link) {

            link.addEventListener(
                "click",
                function () {

                    navigationMenu.classList.remove(
                        "active"
                    );

                    document.body.style.overflow =
                        "";

                }
            );

        }
    );


});