from fastapi import FastAPI

from app.db.database import engine
from app.db.base import Base

# Import Routers
from app.api.auth import router as auth_router
from app.api.incident import router as incident_router

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AegisOps AI",
    version="1.0.0"
)

# Register API Routers
app.include_router(auth_router)
app.include_router(incident_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to AegisOps AI 🚀",
        "status": "Backend is running successfully!"
    }