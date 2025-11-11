"""
Migration script to populate initial series data.
Run with: python -m scripts.populate_series
"""

from sqlmodel import create_engine, Session, select
from app.models.models import Series
from app.config import settings
from datetime import datetime, timezone
import sys

def populate_series():
    """Populate initial series based on university cohorts"""
    
    engine = create_engine(settings.database_url, echo=False)
    
    # Define series data
    series_data = [
        {
            "series_code": "022",
            "name": "2022/2023 Series",
            "description": "Students admitted in 2022 (22/sc/co/xxxx)"
        },
        {
            "series_code": "023",
            "name": "2023/2024 Series",
            "description": "Students admitted in 2023 (23/sc/co/xxxx)"
        },
        {
            "series_code": "024",
            "name": "2024/2025 Series",
            "description": "Students admitted in 2024 (24/sc/co/xxxx)"
        },
        {
            "series_code": "025",
            "name": "2025/2026 Series",
            "description": "Students admitted in 2025 (25/sc/co/xxxx)"
        },
        {
            "series_code": "026",
            "name": "2026/2027 Series",
            "description": "Students admitted in 2026 (26/sc/co/xxxx)"
        },
        {
            "series_code": "027",
            "name": "2027/2028 Series",
            "description": "Students admitted in 2027 (27/sc/co/xxxx)"
        }
    ]
    
    with Session(engine) as session:
        try:
            for data in series_data:
                # Check if series already exists
                existing = session.exec(
                    select(Series).where(Series.series_code == data["series_code"]) # type: ignore
                ).first()
                
                if existing:
                    print(f"⏭️  Series {data['series_code']} already exists. Skipping...")
                    continue
                
                # Create new series
                new_series = Series(
                    series_code=data["series_code"],
                    name=data["name"],
                    description=data["description"],
                    is_active=True,
                    created_at=datetime.now(timezone.utc),
                    created_by=None  # System-created
                )
                
                session.add(new_series)
                print(f"✅ Created series: {data['series_code']} - {data['name']}")
            
            # Commit all changes
            session.commit()
            print("\n✅ All series populated successfully!")
            
            # Display summary
            total_series = len(session.exec(select(Series)).all())
            active_series = len(session.exec(
                select(Series).where(Series.is_active == True)
            ).all())
            
            print(f"\n📊 Summary:")
            print(f"   Total Series: {total_series}")
            print(f"   Active Series: {active_series}")
            
        except Exception as e:
            print(f"❌ Error populating series: {str(e)}")
            session.rollback()
            sys.exit(1)

if __name__ == "__main__":
    populate_series()