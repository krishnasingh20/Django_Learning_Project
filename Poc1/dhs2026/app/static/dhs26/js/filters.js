document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll("[data-filter-group]").forEach(function (group) {

        var targetSelector = group.getAttribute("data-filter-target");
        var cards = document.querySelectorAll(targetSelector);
        var chips = group.querySelectorAll(".filter-chip");

        chips.forEach(function (chip) {

            chip.addEventListener("click", function () {

                chips.forEach(function (c) {
                    c.classList.remove("is-active");
                });

                chip.classList.add("is-active");

                var filter = chip.getAttribute("data-filter");

                cards.forEach(function (card) {

                    if (filter === "all") {
                        card.classList.remove("is-hidden");
                        return;
                    }

                    var tags = (card.getAttribute("data-tags") || "").split(" ");

                    if (tags.indexOf(filter) !== -1) {
                        card.classList.remove("is-hidden");
                    } else {
                        card.classList.add("is-hidden");
                    }

                });

            });

        });

    });

});
