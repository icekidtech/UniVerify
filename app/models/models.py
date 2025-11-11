from sqlmodel import SQLModel, Field # type: ignore
from datetime import datetime, timezone
from typing import Optional

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    phone: str = Field(unique=True)
    reg_number: str = Field(unique=True)
    department: str
    photo_path: str
    passcode: str
    status: str = "pending"
    submitted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    approved_at: Optional[datetime] = None
    approved_by: Optional[int] = None

class Admin(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    password_hash: str
    name: str
    role: str  # "super_admin" or "admin"
    department: Optional[str] = None  # NULL for super_admin, specific dept for admin
    series: Optional[str] = None  # e.g., "2024", NULL for super_admin
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: Optional[int] = None  # super_admin ID
    is_active: bool = True

class WhatsAppGroup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    original_link: str
    is_active: bool = True

class AccessToken(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    group_id: int = Field(foreign_key="whatsappgroup.id")
    token: str
    used: bool = False
    # FIX: Always use timezone-aware datetime
    expires_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AuditLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    admin_id: int = Field(foreign_key="admin.id")
    action: str  # "approve", "reject", "delete"
    target_student_id: int = Field(foreign_key="student.id")
    details: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))