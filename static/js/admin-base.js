// Admin Base Functions

document.addEventListener('DOMContentLoaded', function() {
    // Add active class to current nav link
    const currentLocation = location.pathname;
    const navLinks = document.querySelectorAll('.admin-sidebar a');

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
        }
    });

    // Add confirmation to action buttons
    const actionButtons = document.querySelectorAll('.action-confirm');
    actionButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to proceed?')) {
                e.preventDefault();
            }
        });
    });
});
