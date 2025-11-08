from sqlmodel import create_engine, Session
from app.models.models import Admin, SQLModel
from app.config import settings
from passlib.context import CryptContext
import sys

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_super_admin(email: str, password: str, name: str):
    engine = create_engine(settings.database_url, echo=False)
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        existing = session.query(Admin).filter(Admin.email == email).first()
        if existing:
            print(f"❌ Admin with email {email} already exists!")
            return
        
        super_admin = Admin(
            email=email,
            password_hash=hash_password(password),
            name=name,
            role="super_admin",
            department=None,
            series=None,
            is_active=True
        )
        session.add(super_admin)
        session.commit()
        print(f"✅ Super Admin created successfully!")
        print(f"   Email: {email}")
        print(f"   Name: {name}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python create_super_admin.py <email> <password> <name>")
        print("Example: python create_super_admin.py admin@024series.com MySecurePass123 'Admin Name'")
        sys.exit(1)
    
    email = sys.argv[1]
    password = sys.argv[2]
    name = sys.argv[3]
    
    create_super_admin(email, password, name)