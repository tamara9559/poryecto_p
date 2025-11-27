from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Datos para la conexión a la base de datos (Amazon RDS MySQL)
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 3306
    DB_NAME: str

    # Otros
    APP_NAME: str = "Inventory API"
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

