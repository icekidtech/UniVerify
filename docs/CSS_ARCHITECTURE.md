# CSS Architecture - Faculty of Computing Student Management System

## Overview

The styling system is organized into a modular, maintainable structure that separates concerns and promotes consistency across the application.

## File Hierarchy

```
static/css/
├── global.css              # Base styles for entire application
├── auth.css                # Login and registration pages
├── landing.css             # Homepage/landing page
├── passcode.css            # Passcode backup page
├── dashboard.css           # Student dashboard
├── admin_dashboard.css     # Admin interface
├── bootstrap.min.css       # Bootstrap framework (external)
└── style.css               # Legacy styles (deprecated)
```

## CSS Files Breakdown

### 1. global.css (Core Foundation)
**Purpose**: Provides base styling for entire application

**Sections**:
```css
:root { }                    /* CSS Variables for colors, spacing */
*                           /* Global element reset */
html, body                  /* Base document styles */
body                        /* Background and text colors */
h1, h2, h3, etc           /* Typography hierarchy */
.btn-primary               /* Button variants */
.btn-success, .btn-danger  /* Action buttons */
.btn-warning               /* Warning actions */
.card                      /* Card components */
table                      /* Table styling */
.form-control              /* Form inputs */
.form-label                /* Form labels */
.alert                     /* Alert messages */
.status                    /* Status badges */
footer                     /* Footer styling */
@media queries             /* Responsive design */
```

**Key Features**:
- CSS Variables for brand colors
- Consistent spacing and sizing
- Accessible color contrasts
- Responsive typography

### 2. auth.css (Authentication Pages)
**Purpose**: Styles for login and registration pages

**Sections**:
```css
.auth-container            /* Full-screen background and layout */
.auth-card                 /* Central card container */
.auth-card h1              /* Page title */
.auth-card .subtitle       /* Subtitle text */
.form-group                /* Form field groups */
.form-group input/select   /* Input styling and focus states */
.form-submit-btn           /* Submit button */
.error-message             /* Error message styling */
.auth-footer               /* Footer with links */
.auth-footer a             /* Footer links */
@media queries             /* Mobile responsiveness */
```

**Key Features**:
- Gradient background
- Centered card layout
- Form validation styling
- Error message display
- Mobile-optimized

### 3. landing.css (Homepage)
**Purpose**: Styles for the landing page

**Sections**:
```css
.landing-page              /* Full-page background */
.landing-container         /* Main content container */
.landing-container h1      /* Main heading */
.landing-container p       /* Description text */
.btn-group-custom          /* Button group layout */
.btn-landing               /* Landing page buttons */
.btn-landing-*             /* Button variants */
.landing-features          /* Features section */
.features-list             /* Feature items */
@media queries             /* Responsive design */
```

**Key Features**:
- Smooth animations
- Feature list display
- Responsive buttons
- Mobile-first approach

### 4. passcode.css (Passcode Backup)
**Purpose**: Styles for passcode backup and display page

**Sections**:
```css
.passcode-page             /* Full-page layout */
.passcode-container        /* Container wrapper */
.passcode-card             /* Main card */
.passcode-header           /* Warning header */
.passcode-body             /* Card content */
.passcode-display          /* Code display area */
.passcode-code             /* Monospace code text */
.copy-btn                  /* Copy button */
.warning-box               /* Warning message box */
.warning-box h5            /* Warning title */
.warning-box ul            /* Warning list */
.checkbox-group            /* Checkbox styling */
.continue-btn              /* Continue button */
@media queries             /* Mobile responsiveness */
```

**Key Features**:
- Clear passcode display
- Warning highlighting
- Copy-to-clipboard button
- Confirmation checkbox
- Security messaging

### 5. dashboard.css (Student Dashboard)
**Purpose**: Styles for student dashboard

**Sections**:
```css
.dashboard-header          /* Header section */
.dashboard-grid            /* Grid layout for cards */
.dashboard-card            /* Individual cards */
.dashboard-card h3         /* Card titles */
.status-badge              /* Status display badges */
.dashboard-links           /* Link section */
.links-grid                /* Grid of links */
.link-button               /* Link buttons */
.pending-message           /* Pending notice */
.user-info                 /* User information section */
.info-row                  /* Information rows */
@media queries             /* Mobile responsiveness */
```

**Key Features**:
- Grid-based layout
- Card hover effects
- Status color coding
- User information display
- Responsive design

### 6. admin_dashboard.css (Admin Interface)
**Purpose**: Styles for admin interface and dashboard

**Sections**:
```css
* { }                      /* Global reset */
body                       /* Page background */
.navbar                    /* Top navigation */
.navbar h1                 /* Navbar title */
.admin-user-info           /* User info in navbar */
.admin-container           /* Main container */
.admin-sidebar             /* Left sidebar navigation */
.admin-sidebar a           /* Sidebar links */
.admin-content             /* Main content area */
.dashboard-title           /* Page titles */
.stats-container           /* Stats cards grid */
.card                      /* Stat cards */
.card.blue/green/etc       /* Card color variants */
table                      /* Data tables */
.overview                  /* Overview section */
.activities                /* Activities section */
.quick-actions             /* Quick action buttons */
@media queries             /* Responsive breakpoints */
```

**Key Features**:
- Sidebar navigation
- Stats cards
- Data tables
- Action buttons
- Mobile responsive sidebar

## CSS Variables Reference

```css
:root {
    /* Colors */
    --primary-color: #003366;        /* Main brand color */
    --primary-dark: #0056b3;         /* Hover/active state */
    --success-color: #15361d;        /* Success/approved */
    --warning-color: #ffc107;        /* Warning/pending */
    --danger-color: #dc2626;         /* Error/rejected */
    --light-bg: #f4f6f9;             /* Background color */
    --text-dark: #333;               /* Main text */
    --text-muted: #666;              /* Muted text */
    --border-color: #ddd;            /* Borders */
    --shadow: 0 0 5px rgba(0,0,0,0.1); /* Shadows */
}
```

## Responsive Design Strategy

### Mobile-First Approach
```css
/* Base styles (mobile) */
.element {
    width: 100%;
    display: block;
}

/* Tablet and above */
@media (min-width: 768px) {
    .element {
        width: 50%;
        display: grid;
    }
}

/* Large screens and above */
@media (min-width: 1024px) {
    .element {
        width: 25%;
        display: flex;
    }
}
```

### Breakpoints
```css
@media (max-width: 480px)  /* Mobile phones */
@media (max-width: 768px)  /* Tablets */
@media (max-width: 1024px) /* Small desktops */
/* Default for large desktops */
```

## Component Styling Patterns

### Buttons
```css
.btn {
    background-color: var(--primary-color);
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.btn:hover {
    background-color: var(--primary-dark);
}

/* Size variants */
.btn.btn-sm { padding: 6px 12px; font-size: 12px; }

/* Color variants */
.btn.btn-success { background-color: var(--success-color); }
.btn.btn-warning { background-color: var(--warning-color); }
.btn.btn-danger { background-color: var(--danger-color); }
```

### Forms
```css
.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
}

.form-control {
    width: 100%;
    padding: 12px;
    border: 1px solid var(--border-color);
    border-radius: 6px;
}

.form-control:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(0, 51, 102, 0.1);
}
```

### Cards
```css
.card {
    border-radius: 8px;
    padding: 20px;
    background: white;
    box-shadow: var(--shadow);
}

.card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
```

### Tables
```css
table {
    width: 100%;
    border-collapse: collapse;
}

table th {
    background-color: var(--primary-color);
    color: white;
    padding: 12px;
    text-align: left;
}

table td {
    padding: 10px 12px;
    border-bottom: 1px solid var(--border-color);
}

table tbody tr:hover {
    background-color: #f9fafb;
}
```

## Common CSS Classes

| Class | Purpose | Example |
|-------|---------|---------|
| `.btn-primary` | Primary action button | Save, Submit |
| `.btn-success` | Success action | Approve, Confirm |
| `.btn-danger` | Dangerous action | Delete, Reject |
| `.btn-warning` | Warning action | Caution |
| `.status.approved` | Approved badge | Green status |
| `.status.pending` | Pending badge | Yellow status |
| `.status.rejected` | Rejected badge | Red status |
| `.error-message` | Error display | Form errors |
| `.alert-danger` | Danger alert | Error message |
| `.alert-success` | Success alert | Success message |

## Best Practices

### 1. Use CSS Variables
```css
/* ✓ Good */
color: var(--primary-color);

/* ✗ Avoid */
color: #003366;
```

### 2. Follow Naming Conventions
```css
/* ✓ Good - kebab-case */
.dashboard-card { }
.admin-sidebar { }

/* ✗ Avoid - camelCase or inconsistent */
.dashboardCard { }
.adminSidebar { }
```

### 3. Organize with Comments
```css
/* === Header === */
.header { }

/* === Navigation === */
.navbar { }
.navbar a { }

/* === Main Content === */
.container { }
```

### 4. Mobile-First Media Queries
```css
/* Base mobile styles */
.element { width: 100%; }

/* Larger screens */
@media (min-width: 768px) {
    .element { width: 50%; }
}
```

### 5. Separate Concerns
```css
/* ✓ Good - Separate files */
global.css
auth.css
dashboard.css

/* ✗ Avoid - All in one file */
styles.css (10,000+ lines)
```

## Testing CSS Changes

1. **Desktop (1920x1080)**
   - Main layout
   - Full feature set
   - Desktop navigation

2. **Tablet (768x1024)**
   - Tab/touch navigation
   - Two-column layouts
   - Responsive sidebar

3. **Mobile (375x812)**
   - Single column
   - Touch-friendly buttons
   - Collapsed navigation
   - Readable text

4. **Print View**
   - Hide navigation
   - Optimize colors
   - Page breaks
   - Header/footer

## Performance Considerations

- **CSS file size**: Keep under 50KB per file
- **Specificity**: Keep low (avoid !important)
- **Selectors**: Use efficient selectors (.class, not #id)
- **Animations**: Use transform and opacity for smooth performance
- **Media queries**: Place at end of file or in separate file

## Future Enhancements

- [ ] Implement SASS/LESS preprocessor
- [ ] Add dark mode theme
- [ ] Create print stylesheet
- [ ] Implement CSS Grid for layouts
- [ ] Add animation library
- [ ] Optimize for high DPI displays
- [ ] Implement critical CSS
- [ ] Add performance metrics

---

**Last Updated**: November 8, 2025  
**Status**: Documentation Complete ✓
