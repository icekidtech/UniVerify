# Quick Reference - Styling Guidelines

## Brand Colors

```css
:root {
    --primary-color: #003366;      /* Dark Blue - Main brand */
    --primary-dark: #0056b3;       /* Lighter blue - Hover state */
    --success-color: #15361d;      /* Dark Green - Approved/Success */
    --warning-color: #ffc107;      /* Yellow - Pending/Warning */
    --danger-color: #dc2626;       /* Red - Rejected/Error */
    --light-bg: #f4f6f9;           /* Light Gray - Background */
    --text-dark: #333;             /* Dark Gray - Text */
    --text-muted: #666;            /* Gray - Muted text */
}
```

## CSS File Organization

| File | Purpose | Should Include |
|------|---------|---|
| `global.css` | Base styles for all pages | Buttons, forms, tables, alerts, typography |
| `auth.css` | Login/Register pages | Auth container, forms, error messages |
| `landing.css` | Homepage | Landing card, buttons, features |
| `passcode.css` | Passcode backup page | Passcode display, warning box, checkbox |
| `dashboard.css` | Student dashboard | Cards, grid layout, user info |
| `admin_dashboard.css` | Admin interface | Navbar, sidebar, stats cards, tables |

## How to Style a New Page

1. Create a new CSS file: `static/css/page-name.css`
2. Link it in the HTML file after `global.css`
3. Use CSS variables for colors
4. Follow the responsive breakpoints pattern
5. Remove any inline styles

Example:
```html
<head>
    <link rel="stylesheet" href="/static/css/global.css">
    <link rel="stylesheet" href="/static/css/page-name.css">
</head>
```

## Common CSS Classes

```css
/* Buttons */
.btn { ... }
.btn-primary { background-color: var(--primary-color); }
.btn-success { background-color: var(--success-color); }
.btn-danger { background-color: var(--danger-color); }
.btn-warning { background-color: var(--warning-color); }
.btn-sm { padding: 6px 12px; font-size: 12px; }

/* Status Badges */
.status { display: inline-block; border-radius: 20px; }
.status.approved { background: var(--success-color); color: white; }
.status.pending { background: var(--warning-color); color: #000; }
.status.rejected { background: var(--danger-color); color: white; }

/* Cards */
.card { border-radius: 8px; box-shadow: var(--shadow); }
.card-header { background-color: var(--primary-color); color: white; }

/* Forms */
.form-control { border: 1px solid #ddd; border-radius: 4px; }
.form-control:focus { 
    border-color: var(--primary-color);
    box-shadow: 0 0 0 0.2rem rgba(0, 51, 102, 0.25);
}

/* Alerts */
.alert-danger { background-color: #fee; color: #c33; }
.alert-success { background-color: #efe; color: #3c3; }
.alert-warning { background-color: #ffeaa7; color: #856404; }
.alert-info { background-color: #e7f3ff; color: #004085; }
```

## Responsive Breakpoints

```css
/* Large screens (default) */
/* ... */

/* Tablets (max-width: 1024px) */
@media (max-width: 1024px) {
    /* Adjust layout for tablets */
}

/* Small devices (max-width: 768px) */
@media (max-width: 768px) {
    /* Adjust layout for phones */
}

/* Mobile phones (max-width: 480px) */
@media (max-width: 480px) {
    /* Adjust layout for small phones */
}
```

## JavaScript Best Practices

Place all JavaScript in `static/js/` files, NOT in HTML `<script>` tags.

### Example: Passcode Copy Function
```javascript
// static/js/passcode.js
function copyToClipboard() {
    const passcode = document.querySelector('.passcode-code').textContent.trim();
    navigator.clipboard.writeText(passcode).then(() => {
        alert('Passcode copied!');
    });
}

// Call from HTML with: onclick="copyToClipboard()"
```

### Example: Form Validation
```javascript
// static/js/auth.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    form.addEventListener('submit', function(e) {
        // Validation logic
    });
});
```

## Template Hierarchy

```
base_admin.html (Admin base template)
├── admin/dashboard.html
├── admin/users_request.html
└── admin/users.html

(Student pages don't use a base template currently)
├── index.html
├── login.html
├── register.html
├── passcode_backup.html
└── dashboard.html
```

## Naming Conventions

- CSS Classes: kebab-case (e.g., `.admin-sidebar`, `.dashboard-card`)
- IDs: camelCase (e.g., `id="confirmCheckbox"`)
- CSS Files: kebab-case (e.g., `admin-base.js`)
- Colors: Use variables (e.g., `var(--primary-color)`)

## Adding New Colors

If you need a new color:

1. Add it to `global.css`:
```css
:root {
    --new-color: #HEXCODE;
}
```

2. Use it in your CSS:
```css
.element {
    background-color: var(--new-color);
}
```

## Testing Styles

1. **Desktop**: Test in Chrome DevTools at 1920x1080
2. **Tablet**: Test at 768x1024
3. **Mobile**: Test at 375x812
4. **Dark Theme**: Use browser dark mode testing
5. **Print**: Use Ctrl+P to test print styles

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Color not updating | Clear browser cache (Ctrl+Shift+Delete) |
| Styles not applying | Check CSS specificity, ensure file is linked |
| Layout broken on mobile | Check media queries, test responsive view |
| Inline styles ignored | Remove inline styles, use CSS files instead |

## Helpful Tools

- Chrome DevTools: F12 for inspecting elements
- Color Picker: Use DevTools color picker or online tools
- Responsive Tester: Use DevTools device mode or responsively.app
- CSS Validator: jigsaw.w3.org/css-validator/

---

For more details, see `REBRANDING_SUMMARY.md`
