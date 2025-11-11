document.addEventListener('DOMContentLoaded', function() {
    // Get current page URL path
    const currentPath = window.location.pathname;
    
    // Get all sidebar navigation links
    const sidebarLinks = document.querySelectorAll('.student-sidebar .sidebar-nav-link');
    
    // Remove active class from all links first
    sidebarLinks.forEach(link => {
        link.classList.remove('active');
    });
    
    // Add active class to matching link
    sidebarLinks.forEach(link => {
        const href = link.getAttribute('href');
        
        // Exact match for current path
        if (href === currentPath) {
            link.classList.add('active');
        }
        // Check if current path starts with href (for nested routes)
        else if (currentPath.startsWith(href + '/')) {
            link.classList.add('active');
        }
    });
    
    console.log('Current path:', currentPath);
    console.log('Active links set');
});