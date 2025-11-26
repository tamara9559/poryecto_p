from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database configuration
    DATABASE_URL: str = "mysql+pymysql://user:password@your-rds-endpoint:3306/p-pruebas"
    
    # API configuration
    API_TITLE: str = "Inventory Management System"
    API_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
