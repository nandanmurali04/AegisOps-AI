from fastapi import FastAPI

# Create a FastAPI application
app = FastAPI(
    title="AegisOps AI",
    description="Enterprise AI Operations Copilot",
    version="1.0.0"
)

# Home Route
@app.get("/")
def home():
    return {
        "message": "Welcome to AegisOps AI 🚀",
        "status": "Backend is running successfully!"
    }