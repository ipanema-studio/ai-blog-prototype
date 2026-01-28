from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from . import models, database
from .routers import auth, notebooks, files, notes

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="AMS SW Archive")

# CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(notebooks.router)
app.include_router(files.router)
app.include_router(notes.router)

# Mount static files (uploads)
os.makedirs("static/uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

# Mount frontend build
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(__file__)), "../frontend/dist")
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")

