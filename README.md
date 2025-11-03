# UniVerify

**UniVerify** is a secure, student-led web portal for verifying and onboarding students into the '024 Series WhatsApp Community. It ensures only verified students join departmental and general groups, replacing insecure forms with a custom Python-based system.

## Features

- **Student Registration & Verification**: Form with name, email (uniuyo.edu.ng), department, reg number, and photo. Includes duplicate detection and fuzzy matching.
- **Secure Login & Dashboard**: Email + reg number login, status tracking, and temporary WhatsApp links (7-day expiry, one-time use).
- **Admin Panel**: Role-based access for reviewing submissions, managing links, and viewing stats/audit logs.
- **Security**: JWT tokens, input validation, rate limiting, HTTPS enforcement.

## Tech Stack

- **Backend**: Python 3.11 + FastAPI
- **Frontend**: Jinja2 Templates + Bootstrap 5 + HTMX
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Auth**: OAuth2 + JWT
- **File Storage**: Local (encrypted)
- **Deployment**: Render/Railway/Vercel

## Setup

1. **Clone/Navigate**: `cd /home/icekid/Projects/UniVerify`
2. **Virtual Environment**: `python3.11 -m venv venv && source venv/bin/activate`
3. **Install Dependencies**: `pip install -r requirements.txt`
4. **Environment Variables**: Copy `.env.example` to `.env` and fill in values.
5. **Run**: `uvicorn app.main:app --reload`
6. **Access**: `http://127.0.0.1:8000`

## Roadmap

- **MVP** (June 15–22): Form, Auth, Admin Panel, Temp Links
- **Beta** (June 23–25): SE + CS rollout
- **v1.0** (June 26): Full launch
- **v2.0** (July): Email OTP, PDF badge, analytics

## Contributing

Prepared by Idopise Udoh, Director of Software, '024 Series.

For issues or PRs, contact edwinidopise@gmail.com.

**#024**