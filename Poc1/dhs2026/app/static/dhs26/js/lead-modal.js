document.addEventListener('DOMContentLoaded', function () {

    document.querySelectorAll('[data-modal-open]').forEach(function (btn) {

        btn.addEventListener('click', function () {
            var modal = document.getElementById(btn.dataset.modalOpen);
            if (modal) modal.showModal();
        });

    });

    document.querySelectorAll('[data-modal-close]').forEach(function (btn) {

        btn.addEventListener('click', function () {
            var modal = btn.closest('dialog');
            if (modal) modal.close();
        });

    });

    document.querySelectorAll('dialog.lead-modal').forEach(function (modal) {

        // Click on the backdrop closes the modal
        modal.addEventListener('click', function (e) {
            if (e.target === modal) modal.close();
        });

        // Always reset the form once the modal closes, however it closed
        // (X button, backdrop click, Esc key, or a successful submit).
        modal.addEventListener('close', function () {
            var form = modal.querySelector('form');
            if (form) form.reset();
        });

        // Forms with their own backend handler close themselves once the
        // request finishes. Any other lead-modal form has no backend yet,
        // so it just closes on submit.
        var form = modal.querySelector('form');
        if (form && !form.querySelector('.downloadWorkshopDetail')) {
            form.addEventListener('submit', function (e) {
                e.preventDefault();
                modal.close();
            });
        }

    });


    // Welcome popup — shown once per browser session, shortly after the
    // first page of a visit finishes loading.
    var welcomeModal = document.getElementById('welcomeModal');

    if (welcomeModal && !sessionStorage.getItem('dhs26_welcome_shown')) {

        setTimeout(function () {
            welcomeModal.showModal();
            sessionStorage.setItem('dhs26_welcome_shown', '1');
        }, 3000);

    }

});
