# **UniVerify — Product Requirements Document (PRD)**

**'024 Series WhatsApp Community Verification Portal**  
**Version:** 1.0  
**Date:** June 14, 2025  
**Author:** Idopise Udoh, Director of Software, '024 Series

**Status:** Draft → Chairman Approval Pending

---

## **1\. Executive Summary**

**UniVerify** is a secure, student-led web portal that verifies, onboards, and manages access to the **restructured '024 Series WhatsApp Community** as outlined in the June 14, 2025 memo. It replaces the proposed Google Form with a **custom, secure, and scalable Python-based system** that ensures **only verified students** join departmental and general groups.

This system will:

* Prevent unauthorized access  
* Eliminate duplicate entries  
* Hide original WhatsApp links using **temporary, user-specific redirect URLs**  
* Provide a **student dashboard** and **admin panel**  
* Be fully owned and maintained by the **Software Directorate, '024 Series**

---

## **2\. Objectives**

| Goal | Metric |
| ----- | ----- |
| 100% verified membership | All users pass reg number \+ photo check |
| Zero duplicate entries | Real-time duplicate detection |
| Secure link distribution | No direct access to original WhatsApp links |
| Admin transparency | Full audit trail \+ approval workflow |
| Student UX | Clean, mobile-friendly, \<2 min onboarding |

---

## **3\. Tech Stack**

| Layer | Technology |
| ----- | ----- |
| **Backend** | **Python 3.11 \+ FastAPI** |
| **Frontend** | **Jinja2 Templates \+ Bootstrap 5 \+ HTMX** |
| **Database** | **PostgreSQL** (production), **SQLite** (dev) |
| **Auth** | **OAuth2 (Email \+ Reg Number)** \+ JWT |
| **File Storage** | **Local (encrypted) \+ optional AWS S3** |
| **Deployment** | **Render / Railway / Vercel** |
| **Security** | HTTPS, Rate Limiting, CSRF, Input Sanitization |
| **Extras** | pydantic, SQLModel, python-multipart, passlib, PyJWT |

---

## **4\. User Personas**

| Persona | Needs |
| ----- | ----- |
| **Student ('024 Series)** | Fast form → verify → get WhatsApp link |
| **Admin (Chairman, Execs)** | Review submissions, approve/reject, view stats |
| **Director of Software** | Manage system, deploy updates, audit logs |

---

## **5\. Core Features**

### **5.1 Student Registration & Verification**

**Form Fields:**

\- Full Name (text, required)  
\- Email (uniuyo.edu.ng only, required)  
\- Department (dropdown: SE, CS, IS, DS, CY)  
\- Registration Number (e.g., 24/SC/CO/1234, unique)

\- Recent Photo (JPEG/PNG, \<2MB, face visible)

**Validation Logic (on submit):**

python  
1. Exact match: reg\_number → REJECT  
2. Exact match: email → REJECT  
3. Fuzzy match (85%+): name \+ department → FLAG for review  
4. Photo duplicate (hash check) → REJECT

**Outcome:**

* **Success:** Account created → status \= 'pending' → redirect to login  
* **Failure:** Error message with reason

---

### **5.2 User Login & Dashboard**

**Login:**

* Email \+ Reg Number (treated as password)  
* 2FA via email OTP (optional in v2)

**Student Dashboard (/dashboard):**

text  
Welcome, John Doe (SE)  
Status: Approved | Pending | Rejected

\[If Approved\]  
Your Access Links (expire in 7 days):  
→ Software Engineering Group → \[Join Now\] (temp link)  
→ General Hangout → \[Join Now\]  
→ Tech Community → \[Join Now\]

\[Download Verification Badge\] (PDF)  
---

### **5.3 Secure WhatsApp Link Delivery (Critical)**

**Original WhatsApp links are NEVER exposed.**

#### **Mechanism: Temporary Redirect URLs**

| Step | Action |
| ----- | ----- |
| 1 | Admin uploads **original WhatsApp group links** (per dept \+ general) |
| 2 | On approval → system generates **one-time, user-specific redirect URL** |
| 3 | URL format: https://univerify.024series.com/r/\<token\> |
| 4 | Token contains: user\_id, group\_id, expiry (7 days) → encrypted JWT |
| 5 | On click → validate token → redirect to **original WhatsApp link** → mark as used |

**Prevents:**

* Link sharing with outsiders  
* Link scraping  
* Mass joining

---

### **5.4 Admin Panel (/admin)**

**Access:** Role-based (Chairman, Director, Approved Execs)

**Features:**

* Login with email \+ password  
* Dashboard with stats:  
  * Total submissions  
  * Pending / Approved / Rejected  
  * Dept breakdown (pie chart)  
* Table view of all students:  
  * Name, Reg, Dept, Photo (click to enlarge), Status, Submitted At  
  * Actions: **Approve**, **Reject**, **Resend Link**, **Delete**  
* Bulk actions: Export CSV, Approve All (filtered)  
* Manage WhatsApp Links (upload/edit per group)  
* Audit log: Who approved whom, when

---

## **6\. Data Model (SQLModel)**

python  
class Student(Base):  
    id: int  
    name: str  
    email: str (unique)  
    reg\_number: str (unique)  
    department: str  
    photo\_path: str  
    status: str \= "pending"  \# pending, approved, rejected  
    submitted\_at: datetime  
    approved\_at: Optional\[datetime\]  
    approved\_by: Optional\[int\]  \# admin ID

class WhatsAppGroup(Base):  
    id: int  
    name: str  \# e.g., "Software Engineering"  
    original\_link: str  \# encrypted  
    is\_active: bool

class AccessToken(Base):  
    id: int  
    student\_id: int  
    group\_id: int  
    token: str  \# JWT  
    expires\_at: datetime  
    used: bool \= False  
---

## **7\. Security & Privacy**

| Measure | Implementation |
| ----- | ----- |
| **Data Encryption** | Photo paths encrypted, DB fields hashed |
| **Link Obfuscation** | JWT \+ 7-day expiry \+ one-time use |
| **Input Validation** | Pydantic \+ WTForms-style |
| **Rate Limiting** | 5 submits/hour per IP |
| **HTTPS Only** | Enforced in production |
| **GDPR-like Compliance** | Delete on request, no data sharing |

---

## **8\. UI/UX Flow**

graph TD  
    A\[Landing Page\] \--\> B\[Register Form\]  
    B \--\> C{Validation}  
    C \--\>|Fail| D\[Error Message\]  
    C \--\>|Success| E\[Login Page\]  
    E \--\> F\[Student Dashboard\]  
    F \--\>|Pending| G\[Wait for Approval\]  
    F \--\>|Approved| H\[Temporary Links\]

    H \--\> I\[Click → Redirect → WhatsApp\]

   Admin\[Admin Login\] \--\> J\[Admin Panel\]  
    J \--\> K\[Review → Approve\]

    K \--\> L\[Auto-generate temp links\]

---

## **9\. Non-Functional Requirements**

| Requirement | Target |
| ----- | ----- |
| **Uptime** | 99.9% |
| **Response Time** | \< 300ms |
| **Mobile Support** | 100% responsive |
| **Concurrent Users** | 200+ |
| **Backup** | Daily DB snapshots |

---

## **10\. Roadmap**

| Phase | Timeline | Deliverables |
| ----- | ----- | ----- |
| **MVP** | June 15–22 | Form, Auth, Admin Panel, Temp Links |
| **Beta** | June 23–25 | SE \+ CS rollout, feedback |
| **v1.0** | June 26 | Full launch, all depts |
| **v2.0** | July | Email OTP, PDF badge, analytics |

---

## **11\. Success Metrics**

| KPI | Target |
| ----- | ----- |
| Verification Rate | 95%+ students approved |
| Link Abuse | 0 reported cases |
| Admin Efficiency | \< 2 min per approval |
| Student NPS | \> 8/10 |

---

## **12\. Risks & Mitigations**

| Risk | Mitigation |
| ----- | ----- |
| Students forget login | Allow Reg Number reset via email |
| Link expiry confusion | Clear countdown \+ resend option |
| Photo privacy concerns | Auto-delete after 1 year or on request |
| System downtime | Auto-backup \+ monitoring |

---

## **13\. Appendix**

### **Sample Temp Link Flow**

text  
User clicks: https://univerify.024series.com/r/eyJ1c2VyX2lkIjoxMDIsImdyb3VwX2lkIjo1LCJleHAiOjE3MjkwMDAwMDB9

→ Backend validates JWT  
→ If valid & not used → redirect to:  
   https://chat.whatsapp.com/ABCD1234...  
→ Mark token as used  
---

## **Approval**

**Prepared by:**  
Idopise Udoh  
Director of Software, '024 Series

idopise.udoh@uniuyo.edu.ng

**Approved by:**

---

Chairman, '024 Series

Date: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

**Next Step:** Deploy **MVP demo** by **June 17, 2025** for Chairman review.

**Live URL (demo):** https://demo.univerify.024series.com (to be shared)

---

**Let’s build the most secure, student-run verification system in UniUyo history.**

**\#024Leads**

