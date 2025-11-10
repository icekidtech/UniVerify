from sqlmodel import create_engine, Session, select
from app.models.models import Admin, SQLModel
from app.config import settings
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # Bcrypt has a 72-byte limit
    if len(password.encode('utf-8')) > 72:
        password = password[:72]
    return pwd_context.hash(password)

def create_super_admin():
    # Read super admin details from environment variables
    super_admin_email = getattr(settings, 'super_admin_email', None)
    super_admin_password = getattr(settings, 'super_admin_password', None)
    super_admin_name = getattr(settings, 'super_admin_name', None)
    
    # Validate that all required variables are set
    if not all([super_admin_email, super_admin_password, super_admin_name]):
        print("❌ Error: Missing required environment variables!")
        print("   Please set SUPER_ADMIN_EMAIL, SUPER_ADMIN_PASSWORD, and SUPER_ADMIN_NAME in .env")
        return
    
    engine = create_engine(settings.database_url, echo=False)
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        # Use select() instead of query() for SQLModel
        existing = session.exec(select(Admin).where(Admin.email == super_admin_email)).first()
        if existing:
            print(f"❌ Super Admin with email {super_admin_email} already exists!")
            return
        
        super_admin = Admin(
            email=super_admin_email, # type: ignore
            password_hash=hash_password(super_admin_password), # type: ignore
            name=super_admin_name, # type: ignore
            role="super_admin",
            department=None,
            series=None,
            is_active=True
        )
        session.add(super_admin)
        session.commit()
        print(f"✅ Super Admin created successfully!")
        print(f"   Email: {super_admin_email}")
        print(f"   Name: {super_admin_name}")

if __name__ == "__main__":
    create_super_admin()