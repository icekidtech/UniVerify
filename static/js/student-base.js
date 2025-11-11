document.addEventListener('DOMContentLoaded', function() {
    // Get current page URL
    const currentLocation = location.pathname;
    const sidebarLinks = document.querySelectorAll('.student-sidebar .sidebar-link');

    // Add active class to current nav link
    sidebarLinks.forEach(link => {
        const href = link.getAttribute('href');
        
        // Check if current location matches link href
        if (href === currentLocation) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
});