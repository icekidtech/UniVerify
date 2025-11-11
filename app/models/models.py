from sqlmodel import SQLModel, Field # type: ignore
from datetime import datetime, timezone
from typing import Optional

class Series(SQLModel, table=True):
    """Represents a student series/cohort (e.g., 024, 025)"""
    id: Optional[int] = Field(default=None, primary_key=True)
    series_code: str = Field(unique=True)  # e.g., "024", "025"
    name: str  # e.g., "2024 Series"
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: Optional[int] = None  # super_admin ID
    is_active: bool = True

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    phone: str = Field(unique=True)
    reg_number: str = Field(unique=True)
    department: str
    photo_path: str
    passcode: str
    series_id: Optional[int] = Field(default=None, foreign_key="series.id")  # NEW
    status: str = "pending"  # pending, approved, rejected
    submitted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    approved_at: Optional[datetime] = None
    approved_by: Optional[int] = None
    is_active: bool = True

class Admin(SQLModel, table=True):
    """Now created FROM an existing student account"""
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: Optional[int] = Field(default=None, foreign_key="student.id")  # NEW: link to student
    email: str = Field(unique=True)
    password_hash: str
    name: str
    role: str  # "super_admin", "admin"
    series_id: Optional[int] = Field(default=None, foreign_key="series.id")  # NEW: inherited from student
    department: Optional[str] = None  # specific department in their series
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: Optional[int] = None  # super_admin ID
    is_active: bool = True

class WhatsAppGroup(SQLModel, table=True):
    """Now series-specific"""
    id: Optional[int] = Field(default=None, primary_key=True)
    series_id: Optional[int] = Field(default=None, foreign_key="series.id")  # NEW
    name: str  # e.g., "Software Engineering"
    original_link: str
    created_by: Optional[int] = None  # admin ID
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True

class AccessToken(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    group_id: int = Field(foreign_key="whatsappgroup.id")
    token: str
    expires_at: datetime
    used: bool = False
    used_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AuditLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    admin_id: int = Field(foreign_key="admin.id")
    action: str  # "approved", "rejected", "deleted", "link_created", etc.
    target_student_id: Optional[int] = Field(default=None, foreign_key="student.id")
    details: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))