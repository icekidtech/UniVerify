from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    reg_number: str = Field(unique=True)
    department: str
    photo_path: str
    status: str = "pending"
    submitted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    approved_at: Optional[datetime] = None
    approved_by: Optional[int] = None

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
    expires_at: datetime
    used: bool = False