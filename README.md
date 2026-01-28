# AMS SW Archive

A self-hosted, offline-capable NotebookLM clone for secured environments.

## Architecture
- **Backend**: FastAPI (Python) + SQLite
- **Frontend**: React (Vite)
- **Database**: `backend/ams_archive.db` (Auto-created)
- **File Storage**: `backend/static/uploads/`

## Prerequisites
- Python 3.8+
- Node.js 18+ (only for building frontend)

## Installation

1. **Clone the repository** (or copy folder):
   ```bash
   cd ams-sw-archive
   ```

2. **Setup Backend**:
   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Setup Frontend** (Optional, if you want to rebuild):
   ```bash
   cd ../frontend
   npm install --legacy-peer-deps
   npm run build
   ```

## Running the Application

A convenience script is provided:

```bash
./start.sh
```

This will:
1. Activate the Python virtual environment.
2. Start the FastAPI server on port 8000.
3. Serve the frontend at `http://localhost:8000`.

## Features
- **Authentication**: Register and Login.
- **Notebooks**: Create projects to organize files.
- **Sources**: Upload PDF/Text/Images to the left sidebar.
- **Overview**: manually edit the AI overview using the rich text editor (Center).
- **Notes**: Add manual notes and key takeaways (Right).
