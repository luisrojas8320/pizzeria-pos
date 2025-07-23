from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from .core.config import settings
from .core.database import create_tables, get_db
# from .core.auth import get_current_user  # Temporarily disabled
from .api import auth
# Temporarily disable other imports to isolate the problem
# from .api import orders, purchases, menu, staff, analytics, customers, platforms

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Backend API for Delizzia Pizzería POS System",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    try:
        create_tables()
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        # Don't fail startup, just log the error

# Security
security = HTTPBearer()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Delizzia POS API",
        "version": settings.PROJECT_VERSION,
        "status": "running"
    }


# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}


# Include routers
try:
    app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
    print("✅ Auth router loaded")
except Exception as e:
    print(f"❌ Error loading auth router: {e}")

# Temporarily disable other routers to isolate the problem
# app.include_router(orders.router, prefix=f"{settings.API_V1_STR}/orders", tags=["Orders"])
# app.include_router(purchases.router, prefix=f"{settings.API_V1_STR}/purchases", tags=["Purchases"])
# app.include_router(menu.router, prefix=f"{settings.API_V1_STR}/menu", tags=["Menu"])
# app.include_router(staff.router, prefix=f"{settings.API_V1_STR}/staff", tags=["Staff"])
# app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["Analytics"])
# app.include_router(customers.router, prefix=f"{settings.API_V1_STR}/customers", tags=["Customers"])
# app.include_router(platforms.router, prefix=f"{settings.API_V1_STR}/platforms", tags=["Platforms"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)