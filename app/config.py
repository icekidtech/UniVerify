from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./univerify.db"
    secret_key: str = ""
    jwt_secret_key: str = ""

    model_config = {"env_file": ".env"}

settings = Settings()