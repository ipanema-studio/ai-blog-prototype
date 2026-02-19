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
from fastapi.responses import FileResponse

# Mount frontend build
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(__file__)), "../frontend/dist")
if os.path.exists(frontend_dist):
    # Mount assets specifically
    assets_path = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_path):
        app.mount("/assets", StaticFiles(directory=assets_path), name="assets")
    
    # Serve other static files like vite.svg if they exist, otherwise serve index.html
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # API and static uploads are handled by routers/mounts defined above
        
        # Check if file exists in frontend_dist
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
            
        # Fallback to index.html for SPA routing
        return FileResponse(os.path.join(frontend_dist, "index.html"))

