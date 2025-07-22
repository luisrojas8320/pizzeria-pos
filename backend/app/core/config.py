from pydantic import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://delizzia_user:delizzia_password@localhost:5432/delizzia_pos"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Delizzia POS API"
    PROJECT_VERSION: str = "1.0.0"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000",  # React development server
        "http://localhost:8000",  # FastAPI docs
    ]
    
    # Business settings
    COMMISSION_RATES: dict = {
        "uber_eats": 0.30,  # 30% commission
        "pedidos_ya": 0.28,  # 28% commission
        "bis": 0.25,  # 25% commission
        "phone": 0.0,  # No commission for direct orders
        "whatsapp": 0.0,  # No commission for WhatsApp orders
    }
    
    # Packaging costs (USD)
    PACKAGING_COSTS: dict = {
        "small_box": 0.15,
        "medium_box": 0.20,
        "large_box": 0.25,
        "drinks": 0.05,
        "utensils": 0.03,
    }
    
    # Timezone
    TIMEZONE: str = "America/Guayaquil"
    
    # Redis for caching and celery
    REDIS_URL: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()