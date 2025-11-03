# UniVerify Frontend Pages Specification

This document lists all the frontend pages (static files/templates) required for the UniVerify project. Each page should be implemented as a Jinja2 template with Bootstrap 5 styling. The second developer should use this as a checklist for building and styling all static files.

---

## 1. Public Pages

- **Landing Page**  
  `index.html`  
  - Welcome message, project description  
  - Buttons: Register, Login

- **Student Registration**  
  `register.html`  
  - Registration form: name, email, reg number, department, photo upload  
  - Error display section

- **Registration Success**  
  `register_success.html`  
  - Confirmation message  
  - Button: Redirect to Student Dashboard

- **Login Page**  
  `login.html`  
  - Login form: email, reg number  
  - Error display section

---

## 2. Student Pages

- **Dashboard**  
  `dashboard.html`  
  - Welcome message with name and department  
  - Status display: Pending, Approved, Rejected  
  - If Approved: List of WhatsApp group links (one-time use)  
  - If Pending: Waiting message  
  - If Rejected: Message (handled on login page)

- **Error Page (Generic)**  
  `error.html`  
  - Display error messages for unexpected issues

---

## 3. Admin Pages 

- **Admin Login**  
  `admin_login.html`  
  - Admin authentication form

- **Admin Dashboard**  
  `admin_dashboard.html`  
  - Stats: total submissions, status breakdown, department breakdown  
  - Table of students: name, reg number, department, photo, status, actions (approve/reject/delete)

- **WhatsApp Group Management**  
  `group_management.html`  
  - Add/edit/delete WhatsApp group links

- **Audit Log**  
  `audit_log.html`  
  - Table of approval/rejection actions

---

## 4. Miscellaneous

- **404 Not Found**  
  `404.html`  
  - Friendly message for missing pages

- **403 Forbidden**  
  `403.html`  
  - Message for unauthorized access

---

## Notes

- All templates should extend a base layout if possible (`base.html`) for consistent header/footer.
- Use Bootstrap 5 for all styling.
- Ensure forms have proper validation and error display sections.
- Use placeholder data for dynamic sections; backend will inject real data.

---

**Deliverable:**  
All listed HTML files, styled and ready for backend integration.