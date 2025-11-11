"""Utility functions for UniVerify"""

from sqlmodel import Session, select
from app.models.models import Series

def extract_series_from_reg_number(reg_number: str) -> str:
    """
    Extract series code from registration number.
    Example: "24/sc/co/001" → "024"
    """
    try:
        parts = reg_number.split("/")
        if parts:
            year_code = parts[0].strip()
            # Pad with 0 if needed: "24" → "024"
            return f"0{year_code}" if len(year_code) == 2 else year_code
    except Exception:
        pass
    return None # type: ignore

def get_series_by_code(session: Session, series_code: str):
    """Get series by code (e.g., '024')"""
    return session.exec(select(Series).where(Series.series_code == series_code)).first()

def assign_series_to_student(session: Session, student, reg_number: str): # type: ignore
    """Auto-assign series to student based on reg number"""
    series_code = extract_series_from_reg_number(reg_number)
    if series_code:
        series = get_series_by_code(session, series_code)
        if series:
            student.series_id = series.id
            return student # type: ignore
    return student # type: ignore