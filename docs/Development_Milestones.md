# UniVerify Development Milestones

**Project:** UniVerify — Secure Student Verification Portal  
**Version:** 1.0  
**Date:** October 30, 2025  
**Author:** Udoh, Idopise Edwin (based on PRD roadmap)

This document outlines the key milestones for developing UniVerify, derived from the Product Requirements Document (PRD). Each milestone includes deliverables, timelines, and success criteria to ensure structured progress toward the MVP and beyond.

## Overview
UniVerify aims to provide a secure, student-led portal for verifying and onboarding '024 Series students into WhatsApp communities. Development follows an iterative approach, starting with core features and expanding to enhancements.

## Milestones

### Milestone 1: Project Setup and Core Infrastructure (Week 1: Oct 30 - Nov 5, 2025)
**Objective:** Establish the foundational tech stack and basic app structure.  
**Deliverables:**
- Set up FastAPI app with Jinja2 templates, Bootstrap 5, and HTMX.
- Configure database (SQLite for dev, PostgreSQL for prod) using SQLModel.
- Implement basic settings and environment variables.
- Create initial folder structure (app/, static/, templates/, docs/).
- Add basic landing page and routing.

**Success Criteria:** App runs locally without errors; basic GET endpoint responds.

### Milestone 2: Student Registration and Validation (Week 2: Nov 6 - Nov 12, 2025)
**Objective:** Build the student registration form with validation logic.  
**Deliverables:**
- Create registration form (name, email, department, reg number, photo upload).
- Implement validation: exact matches for reg number/email, fuzzy matching for name+dept, photo hash checks.
- Store submissions in database with status 'pending'.
- Add error handling and user feedback.

**Success Criteria:** Form submits successfully for valid inputs; duplicates are rejected; data stored correctly.

### Milestone 3: Authentication and Student Dashboard (Week 3: Nov 13 - Nov 19, 2025)
**Objective:** Implement login system and user dashboard.  
**Deliverables:**
- Add OAuth2/JWT-based login using email + reg number.
- Create student dashboard showing status (pending/approved/rejected).
- Display temporary WhatsApp links for approved users (with 7-day expiry).
- Integrate photo upload and storage (local, encrypted).

**Success Criteria:** Users can register, log in, and view dashboard; approved users see functional temp links.

### Milestone 4: Admin Panel and Approval Workflow (Week 4: Nov 20 - Nov 26, 2025)
**Objective:** Develop admin features for reviewing and managing submissions.  
**Deliverables:**
- Build admin login and role-based access.
- Create admin dashboard with stats, table view of students, and actions (approve/reject).
- Implement WhatsApp group link management (upload/edit original links).
- Add audit logging for approvals.

**Success Criteria:** Admins can log in, review submissions, and approve/reject; stats update in real-time.

### Milestone 5: Secure Link Generation and Redirect (Week 5: Nov 27 - Dec 3, 2025)
**Objective:** Implement temporary, user-specific redirect URLs for WhatsApp links.  
**Deliverables:**
- Generate JWT-based tokens on approval (user_id, group_id, expiry).
- Create redirect endpoint (/r/<token>) that validates and redirects to original link.
- Mark tokens as used after one-time access.
- Ensure links expire after 7 days.

**Success Criteria:** Clicking temp link redirects to WhatsApp; prevents reuse and sharing.

### Milestone 6: MVP Testing and Deployment (Week 6: Dec 4 - Dec 10, 2025)
**Objective:** Test, refine, and deploy the MVP.  
**Deliverables:**
- Conduct unit tests and integration testing.
- Add security measures (rate limiting, HTTPS, input sanitization).
- Deploy to staging (e.g., Render/Railway).
- Gather feedback from initial users (SE/CS depts).

**Success Criteria:** MVP demo live; 95% verification rate in testing; no critical bugs.

### Milestone 7: Beta Rollout and Full Launch (Week 7: Dec 11 - Dec 17, 2025)
**Objective:** Roll out to beta users and prepare for full launch.  
**Deliverables:**
- Enable for SE and CS departments.
- Monitor usage, fix issues based on feedback.
- Expand to all departments.
- Finalize v1.0 features.

**Success Criteria:** Full launch on Dec 17; all depts onboarded; metrics meet targets (e.g., 95% approval rate).

### Milestone 8: v2.0 Enhancements (Week 8+: Dec 18, 2025 onward)
**Objective:** Add advanced features post-launch.  
**Deliverables:**
- Implement email OTP for 2FA.
- Generate PDF verification badges.
- Add analytics and reporting.
- Optimize for performance and scalability.

**Success Criteria:** v2.0 deployed; user NPS >8/10; uptime 99.9%.

## Risk Management
- **Delays in Setup:** Mitigate by using pre-configured templates.
- **Security Issues:** Regular code reviews and testing.
- **Feedback Loops:** Weekly check-ins with stakeholders.

## Next Steps
- Assign tasks to team members.
- Set up version control and CI/CD pipelines.
- Begin with Milestone 1 immediately.

For detailed requirements, refer to [UniVerify — Product Requirements Document (PRD)](/home/icekid/Projects/UniVerify/docs/UniVerify — Product Requirements Document (PRD).md).