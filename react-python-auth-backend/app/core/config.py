from pydantic import BaseSettings

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "React Python Auth Backend"
    APP_VERSION: str = "1.0.0"
    
    # Database settings
    DATABASE_URL: str
    
    # Security settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()