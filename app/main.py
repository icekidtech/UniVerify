from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlmodel import create_engine, Session, select
from app.models.models import Student, WhatsAppGroup, AccessToken, Admin, AuditLog
from app.config import settings
from passlib.context import CryptContext
import hashlib
from difflib import SequenceMatcher
import os
import logging
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
import secrets
import string

# Enable debugging
logging.basicConfig(level=logging.DEBUG)

app = FastAPI(title="UniVerify", debug=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Database setup
engine = create_engine(settings.database_url, echo=True)
# Create tables
from sqlmodel import SQLModel
SQLModel.metadata.create_all(engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def populate_groups():
    with Session(engine) as session:
        if not session.exec(select(WhatsAppGroup)).first():
            groups = [
                WhatsAppGroup(name="Software Engineering", original_link="https://chat.whatsapp.com/SElink", is_active=True),
                WhatsAppGroup(name="Computer Science", original_link="https://chat.whatsapp.com/CSlink", is_active=True),
                WhatsAppGroup(name="General Hangout", original_link="https://chat.whatsapp.com/General", is_active=True),
            ]
            for g in groups:
                session.add(g)
            session.commit()

populate_groups()

def generate_passcode(length: int = 12):
    """Generate a unique alphanumeric passcode"""
    characters = string.ascii_uppercase + string.digits
    passcode = ''.join(secrets.choice(characters) for _ in range(length))
    return passcode

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(
    data: dict[str, str], 
    expires_delta: Optional[timedelta] = None, 
    token_type: str = "student"
) -> str:
    to_encode: dict[str, str | int] = data.copy() # type: ignore
    to_encode["type"] = token_type
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": int(expire.timestamp())})
    encoded_jwt: str = jwt.encode(to_encode, settings.jwt_secret_key, algorithm="HS256")
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# ============= STUDENT ROUTES =============

@app.get("/")
async def landing_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request}) # type: ignore

@app.get("/register")
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request}) # type: ignore

@app.post("/register")
async def register(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    reg_number: str = Form(...),
    department: str = Form(...),
    photo: UploadFile = File(...),
):
    errors = []

    # Basic validations
    if not email.endswith("@gmail.com"):
        errors.append("Email must be from gmail.com domain.") # type: ignore
    if department not in ["Software Engineering", "Computer Science", "Information Systems", "Data Science", "Cybersecurity"]:
        errors.append("Invalid department.") # type: ignore
    if not photo.filename or not photo.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        errors.append("Photo must be PNG or JPEG.") # type: ignore
    if photo.size and photo.size > 2 * 1024 * 1024:
        errors.append("Photo size must be less than 2MB.") # type: ignore
    if not phone or len(phone.replace('+', '').replace(' ', '')) < 10:
        errors.append("Phone number must be valid.") # type: ignore

    if errors:
        return templates.TemplateResponse("register.html", {"request": request, "errors": errors}) # type: ignore # type: ignore

    with Session(engine) as session:
        # Check exact matches
        if session.exec(select(Student).where(Student.reg_number == reg_number)).first():
            errors.append("Registration number already exists.") # type: ignore
        if session.exec(select(Student).where(Student.email == email)).first():
            errors.append("Email already exists.") # type: ignore
        if session.exec(select(Student).where(Student.phone == phone)).first():
            errors.append("Phone number already exists.") # type: ignore

        if errors:
            return templates.TemplateResponse("register.html", {"request": request, "errors": errors}) # type: ignore

        # Fuzzy match name + department (85%+)
        existing_students = session.exec(select(Student)).all()
        for student in existing_students:
            if SequenceMatcher(None, name.lower(), student.name.lower()).ratio() > 0.85 and department == student.department:
                errors.append("Potential duplicate: similar name and department found.") # type: ignore
                break

        # Photo hash check
        photo_content = await photo.read()
        photo_hash = hashlib.sha256(photo_content).hexdigest()
        for student in existing_students:
            if student.photo_path and os.path.exists(student.photo_path):
                with open(student.photo_path, "rb") as f:
                    existing_hash = hashlib.sha256(f.read()).hexdigest()
                if existing_hash == photo_hash:
                    errors.append("Photo already used.") # type: ignore # type: ignore
                    break

        if errors:
            return templates.TemplateResponse("register.html", {"request": request, "errors": errors}) # type: ignore

        # Save photo
        os.makedirs("static/uploads", exist_ok=True)
        sanitized_reg = reg_number.replace('/', '_').replace('\\', '_')
        photo_filename = f"{sanitized_reg}_{photo.filename}"
        photo_path = f"static/uploads/{photo_filename}"
        with open(photo_path, "wb") as f:
            f.write(photo_content)

        # Generate unique passcode
        passcode = generate_passcode()

        # Create student with passcode
        student = Student(
            name=name,
            email=email,
            phone=phone,
            reg_number=reg_number,
            department=department,
            photo_path=photo_path,
            passcode=passcode
        )
        session.add(student)
        session.commit()

        # Redirect to passcode backup page
        return templates.TemplateResponse("passcode_backup.html", {"request": request, "passcode": passcode}) # type: ignore

@app.get("/login")
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request}) # type: ignore

@app.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    reg_number: str = Form(...),
    passcode: str = Form(...),
):
    with Session(engine) as session:
        student = session.exec(select(Student).where(
            Student.email == email,
            Student.reg_number == reg_number,
            Student.passcode == passcode
        )).first()
        
        if not student:
            return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials or passcode."}) # type: ignore

        if student.status == "rejected":
            session.delete(student)
            session.commit()
            return templates.TemplateResponse("login.html", {"request": request, "error": "Your account has been rejected and deleted."}) # type: ignore

        # Create Access token for users
        access_token = create_access_token(data={"sub": str(student.id)}, expires_delta=timedelta(days=7), token_type="student")
        response = RedirectResponse(url="/dashboard", status_code=303)
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return response

def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = verify_token(token)
    if not payload or payload.get("type") != "student":
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = int(payload["sub"])
    with Session(engine) as session:
        student = session.get(Student, user_id)
        if not student:
            raise HTTPException(status_code=401, detail="User not found")
        return student

@app.get("/dashboard")
async def dashboard(request: Request, current_user: Student = Depends(get_current_user)):
    links = []
    if current_user.status == "approved":
        with Session(engine) as session:
            groups = session.exec(select(WhatsAppGroup).where(WhatsAppGroup.is_active == True)).all()
            for group in groups:
                existing_token = session.exec(select(AccessToken).where(
                    AccessToken.student_id == current_user.id,
                    AccessToken.group_id == group.id,
                    AccessToken.used == False
                )).first()
                if existing_token and existing_token.expires_at > datetime.now(timezone.utc):
                    token = existing_token.token
                else:
                    token_data = {"student_id": current_user.id, "group_id": group.id}
                    token = jwt.encode(token_data, settings.jwt_secret_key, algorithm="HS256")
                    access_token = AccessToken(
                        student_id=current_user.id, # type: ignore
                        group_id=group.id, # type: ignore
                        token=token,
                        expires_at=datetime.now(timezone.utc) + timedelta(days=7)
                    )
                    session.add(access_token)
                    session.commit()
                links.append({"name": group.name, "url": f"/r/{token}"}) # type: ignore
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": current_user, "links": links}) # type: ignore # type: ignore

@app.get("/r/{token}")
async def redirect_link(token: str):
    payload = verify_token(token)
    if not payload or "student_id" not in payload or "group_id" not in payload:
        raise HTTPException(status_code=400, detail="Invalid token")
    student_id = payload["student_id"] # type: ignore # type: ignore
    group_id = payload["group_id"]
    with Session(engine) as session:
        token_obj = session.exec(select(AccessToken).where(AccessToken.token == token)).first()
        if not token_obj or token_obj.used:
            raise HTTPException(status_code=400, detail="Token already used or invalid")
        group = session.get(WhatsAppGroup, group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        token_obj.used = True
        session.commit()
        return RedirectResponse(url=group.original_link)

# ============= ADMIN ROUTES =============

@app.get("/admin/login")
async def admin_login_form(request: Request):
    return templates.TemplateResponse("admin/login.html", {"request": request}) # type: ignore

@app.post("/admin/login")
async def admin_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
):
    with Session(engine) as session:
        admin = session.exec(select(Admin).where(Admin.email == email, Admin.is_active == True)).first()
        
        if not admin or not verify_password(password, admin.password_hash):
            return templates.TemplateResponse("admin/login.html", {"request": request, "error": "Invalid email or password."}) # type: ignore

        admin_token = create_access_token(data={"sub": str(admin.id), "role": admin.role}, expires_delta=timedelta(days=30), token_type="admin")
        response = RedirectResponse(url="/admin/dashboard", status_code=303)
        response.set_cookie(key="admin_token", value=admin_token, httponly=True)
        return response

def get_current_admin(request: Request):
    token = request.cookies.get("admin_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = verify_token(token)
    if not payload or payload.get("type") != "admin":
        raise HTTPException(status_code=401, detail="Invalid token")
    admin_id = int(payload["sub"])
    with Session(engine) as session:
        admin = session.get(Admin, admin_id)
        if not admin or not admin.is_active:
            raise HTTPException(status_code=401, detail="Admin not found or inactive")
        return admin

@app.get("/admin/dashboard")
async def admin_dashboard(request: Request, current_admin: Admin = Depends(get_current_admin)):
    with Session(engine) as session:
        if current_admin.role == "super_admin":
            total_students = len(session.exec(select(Student)).all())
            pending_count = len(session.exec(select(Student).where(Student.status == "pending")).all())
            approved_count = len(session.exec(select(Student).where(Student.status == "approved")).all())
            rejected_count = len(session.exec(select(Student).where(Student.status == "rejected")).all())
        else:
            # Regular admin can only see their department/series
            students = session.exec(select(Student).where(
                Student.department == current_admin.department
            )).all()
            total_students = len(students)
            pending_count = len([s for s in students if s.status == "pending"])
            approved_count = len([s for s in students if s.status == "approved"])
            rejected_count = len([s for s in students if s.status == "rejected"])

        stats = {
            "total": total_students,
            "pending": pending_count,
            "approved": approved_count,
            "rejected": rejected_count
        }

    return templates.TemplateResponse("admin/dashboard.html", { # type: ignore # type: ignore
        "request": request,
        "admin": current_admin,
        "stats": stats
    })

@app.get("/admin/requests")
async def admin_requests(request: Request, current_admin: Admin = Depends(get_current_admin)):
    with Session(engine) as session:
        if current_admin.role == "super_admin":
            students = session.exec(select(Student).where(Student.status == "pending")).all()
        else:
            students = session.exec(select(Student).where(
                Student.status == "pending",
                Student.department == current_admin.department
            )).all()

    return templates.TemplateResponse("admin/users_request.html", { # type: ignore
        "request": request,
        "admin": current_admin,
        "students": students
    })

@app.post("/admin/approve/{student_id}")
async def approve_student(request: Request, student_id: int, current_admin: Admin = Depends(get_current_admin)):
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Permission check
        if current_admin.role == "admin" and student.department != current_admin.department:
            raise HTTPException(status_code=403, detail="Not authorized to approve this student")

        student.status = "approved"
        student.approved_at = datetime.now(timezone.utc)
        student.approved_by = current_admin.id

        audit = AuditLog(
            admin_id=current_admin.id, # type: ignore
            action="approve",
            target_student_id=student.id # type: ignore
        )
        session.add(audit)
        session.commit()

    return RedirectResponse(url="/admin/requests", status_code=303)

@app.post("/admin/reject/{student_id}")
async def reject_student(request: Request, student_id: int, current_admin: Admin = Depends(get_current_admin)):
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Permission check - only super_admin can reject, or admin from same department
        if current_admin.role == "admin" and student.department != current_admin.department:
            raise HTTPException(status_code=403, detail="Not authorized to reject this student")

        student.status = "rejected"

        audit = AuditLog(
            admin_id=current_admin.id, # type: ignore
            action="reject",
            target_student_id=student.id # type: ignore
        )
        session.add(audit)
        session.commit()

    return RedirectResponse(url="/admin/requests", status_code=303)

@app.get("/admin/users")
async def admin_users(request: Request, current_admin: Admin = Depends(get_current_admin)):
    with Session(engine) as session:
        if current_admin.role == "super_admin":
            students = session.exec(select(Student)).all()
        else:
            students = session.exec(select(Student).where(
                Student.department == current_admin.department
            )).all()

    return templates.TemplateResponse("admin/users.html", { # type: ignore
        "request": request,
        "admin": current_admin,
        "students": students
    })

@app.get("/admin/logout")
async def admin_logout(request: Request):
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("admin_token")
    return response

@app.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    return response

# ============= SETTINGS ROUTES (STUDENT & ADMIN) =============

@app.get("/settings")
async def settings_page(request: Request):
    """Display settings page for logged-in user"""
    # Try admin token first
    admin_token = request.cookies.get("admin_token")
    if admin_token:
        payload = verify_token(admin_token)
        if payload and payload.get("type") == "admin":
            admin_id = int(payload["sub"])
            with Session(engine) as session:
                admin = session.get(Admin, admin_id)
                if admin and admin.is_active:
                    return templates.TemplateResponse("settings.html", { # type: ignore
                        "request": request,
                        "user": admin,
                        "user_type": "admin"
                    })
    
    # Fall back to student token
    student_token = request.cookies.get("access_token")
    if student_token:
        payload = verify_token(student_token)
        if payload and payload.get("type") == "student":
            user_id = int(payload["sub"])
            with Session(engine) as session:
                student = session.get(Student, user_id)
                if student:
                    return templates.TemplateResponse("settings.html", { # type: ignore
                        "request": request,
                        "user": student,
                        "user_type": "student"
                    })
    
    return RedirectResponse(url="/login", status_code=302)

@app.post("/settings/update")
async def update_settings(
    request: Request, 
    name: str = Form(...), 
    email: str = Form(...),
    phone: str = Form(None),  # Add this parameter
    department: str = Form(None)  # Add this parameter
):
    """Update user settings for student or admin"""
    # Check admin token
    admin_token = request.cookies.get("admin_token")
    if admin_token:
        payload = verify_token(admin_token)
        if payload and payload.get("type") == "admin":
            admin_id = int(payload["sub"])
            with Session(engine) as session:
                admin = session.get(Admin, admin_id)
                if admin:
                    admin.name = name
                    admin.email = email
                    if department:  # Use the parameter directly
                        admin.department = department
                    session.add(admin)
                    session.commit()
                    return RedirectResponse(url="/settings", status_code=303)
    
    # Check student token
    student_token = request.cookies.get("access_token")
    if student_token:
        payload = verify_token(student_token)
        if payload and payload.get("type") == "student":
            user_id = int(payload["sub"])
            with Session(engine) as session:
                student = session.get(Student, user_id)
                if student:
                    student.name = name
                    student.email = email
                    if phone:  # Use the parameter directly
                        student.phone = phone
                    session.add(student)
                    session.commit()
                    return RedirectResponse(url="/settings", status_code=303)
    
    raise HTTPException(status_code=401, detail="Not authenticated")

@app.post("/settings/regenerate-passcode")
async def regenerate_passcode(request: Request, current_user: Student = Depends(get_current_user)): # type: ignore
    """Regenerate student passcode"""
    new_passcode = generate_passcode()
    
    with Session(engine) as session:
        student = session.get(Student, current_user.id)
        if student:
            student.passcode = new_passcode
            session.add(student)
            session.commit()
            return {"success": True, "passcode": new_passcode} # type: ignore
    
    return {"success": False, "message": "Error regenerating passcode"} # type: ignore

# ============= ADMIN MANAGEMENT ROUTES (SUPER ADMIN ONLY) =============

@app.get("/admin/manage-admins")
async def manage_admins(request: Request, current_admin: Admin = Depends(get_current_admin)):
    """Display admin management page (super admin only)"""
    if current_admin.role != "super_admin":
        raise HTTPException(status_code=403, detail="Only super admins can access this page")

    with Session(engine) as session:
        admins = session.exec(select(Admin)).all()

    return templates.TemplateResponse("admin/manage_admins.html", { # pyright: ignore[reportUnknownMemberType]
        "request": request,
        "current_admin": current_admin,
        "admins": admins
    })

@app.post("/admin/add-admin")
async def add_admin(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    department: str = Form(None),
    is_active: str = Form("true"),
    current_admin: Admin = Depends(get_current_admin)
):
    """Add new admin (super admin only)"""
    if current_admin.role != "super_admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    if role not in ["admin", "super_admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    with Session(engine) as session:
        # Check if email exists
        if session.exec(select(Admin).where(Admin.email == email)).first():
            raise HTTPException(status_code=400, detail="Email already exists")

        new_admin = Admin(
            name=name,
            email=email,
            password_hash=hash_password(password),
            role=role,
            department=department,
            is_active=is_active.lower() == "true"
        )
        session.add(new_admin)
        session.commit()

    return RedirectResponse(url="/admin/manage-admins", status_code=303)

@app.post("/admin/update-admin/{admin_id}")
async def update_admin(
    request: Request,
    admin_id: int,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(None),
    role: str = Form(...),
    department: str = Form(None),
    is_active: str = Form("true"),
    current_admin: Admin = Depends(get_current_admin)
):
    """Update admin details (super admin only)"""
    if current_admin.role != "super_admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    with Session(engine) as session:
        admin = session.get(Admin, admin_id)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")

        admin.name = name
        admin.email = email
        admin.role = role
        admin.department = department
        admin.is_active = is_active.lower() == "true"
        
        if password:
            admin.password_hash = hash_password(password)

        session.add(admin)
        session.commit()

    return RedirectResponse(url="/admin/manage-admins", status_code=303)

@app.get("/admin/get-admin/{admin_id}")
async def get_admin_data(admin_id: int, current_admin: Admin = Depends(get_current_admin)) -> dict[str, str | int | bool]:
    """Fetch admin data for modal edit (super admin only)"""
    if current_admin.role != "super_admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    with Session(engine) as session:
        admin = session.get(Admin, admin_id)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")

        return {
            "id": admin.id, # type: ignore
            "name": admin.name,
            "email": admin.email,
            "role": admin.role,
            "department": admin.department or "",
            "is_active": admin.is_active
        }

@app.post("/admin/toggle-admin-status/{admin_id}")
async def toggle_admin_status(
    request: Request,
    admin_id: int,
    current_admin: Admin = Depends(get_current_admin)
):
    """Toggle admin active/inactive status (super admin only)"""
    if current_admin.role != "super_admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    data = await request.json()
    
    with Session(engine) as session:
        admin = session.get(Admin, admin_id)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")

        admin.is_active = data.get("is_active", admin.is_active)
        session.add(admin)
        session.commit()

    return {"success": True}

@app.delete("/admin/delete-admin/{admin_id}")
async def delete_admin(
    admin_id: int,
    current_admin: Admin = Depends(get_current_admin)
):
    """Delete admin (super admin only)"""
    if current_admin.role != "super_admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    with Session(engine) as session:
        admin = session.get(Admin, admin_id)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")

        if admin.id == current_admin.id:
            raise HTTPException(status_code=400, detail="Cannot delete your own account")

        session.delete(admin)
        session.commit()

    return {"success": True}

@app.get("/admin/settings")
async def admin_settings(request: Request, current_admin: Admin = Depends(get_current_admin)):
    """Display settings page for logged-in admin"""
    return templates.TemplateResponse("settings.html", { # type: ignore
        "request": request,
        "user": current_admin,
        "user_type": "admin"
    })