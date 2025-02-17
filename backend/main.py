from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from controllers import fashion_controller, video_controller, scholarship_controller
from config import settings

app = FastAPI(
    title="John Allen's Fashion Platform",
    description="Fashion, Video, and Scholarship Platform API",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongodb = app.mongodb_client[settings.MONGODB_DB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

# Include routers
app.include_router(fashion_controller.router, prefix="/api/fashion", tags=["Fashion"])
app.include_router(video_controller.router, prefix="/api/videos", tags=["Videos"])
app.include_router(scholarship_controller.router, prefix="/api/scholarships", tags=["Scholarships"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to John Allen's Fashion Platform API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }
