from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./univerify.db"
    secret_key: str = ""
    jwt_secret_key: str = ""
    super_admin_email: str = ""
    super_admin_password: str = ""
    super_admin_name: str = ""

    model_config = {"env_file": ".env"}

settings = Settings()