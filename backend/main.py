from typing import Annotated
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI
from backend.database.config import create_db_and_tables
from backend.router import todo_router
from backend.router import arbeiter_router
from backend.router import bearbeiter_router
from backend.router import status_router
from backend.router import topics_router
from backend.router import misc_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle handler that runs on startup and shutdown.
    - On startup: Creates database tables
    - On shutdown: Automatically cleans up resources after yield
    """
    create_db_and_tables()
    yield

# Initialize FastAPI application with the lifecycle manager
app = FastAPI(lifespan=lifespan)
app.include_router(todo_router.router)
app.include_router(arbeiter_router.router)
app.include_router(bearbeiter_router.router)
app.include_router(status_router.router)
app.include_router(topics_router.router)
app.include_router(misc_router.router)

# CORS Configuration
# Defines which origins (frontend URLs) are allowed to access this API
origins = [
    "http://localhost:5173",  # Frontend dev server (e.g., Vite)
    "http://localhost:8000",  # API server
]

# Add CORS middleware to allow cross-origin requests from frontend applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     # Only specified origins can access the API
    allow_credentials=True,    # Allow cookies to be included in requests
    allow_methods=["*"],       # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],       # Allow all HTTP headers in requests
)