from typing import Annotated
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI
from backend.database.config import Session, get_session, create_db_and_tables

# Type annotation for dependency injection of database sessions
# This allows FastAPI to automatically provide database sessions to route handlers
SessionDep = Annotated[Session, Depends(get_session)]

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

# CORS Configuration
# Defines which origins (frontend URLs) are allowed to access this API
origins = [
    "http://localhost:5173",  # Frontend dev server (e.g., Vite)
    "http://localhost:8000",  # Alternative frontend or API server
]

# Add CORS middleware to allow cross-origin requests from frontend applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     # Only specified origins can access the API
    allow_credentials=True,    # Allow cookies to be included in requests
    allow_methods=["*"],       # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],       # Allow all HTTP headers in requests
)