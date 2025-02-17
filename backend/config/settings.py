from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "John Allen's Fashion Platform"
    DEBUG: bool = False
    
    # MongoDB Settings
    MONGODB_URL: str = "mongodb+srv://astudentoflife:faLMPOjzHwPYt5DT@cluster0.jcmel.mongodb.net/fashion_platform?retryWrites=true&w=majority"
    MONGODB_DB_NAME: str = "fashion_platform"
    
    # JWT Settings
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Google Cloud Storage
    GCS_BUCKET_NAME: str = "john-allens-fashion"
    
    # CORS Settings
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",  # Vite dev server
        "http://localhost:4173",  # Vite preview
        "https://johnallens.com"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
