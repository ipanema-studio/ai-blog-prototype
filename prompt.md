# Role
Act as a Senior Full-Stack Developer proficient in Python and the "Antigravity" framework.

# Project Overview
Build a self-hosted web application named "Internal NotebookLM".
The goal is to replicate the user interface and user experience of Google's NotebookLM, but strictly for an offline, high-security internal environment.

# Critical Constraints (Security)
1. NO external API calls allowed (No OpenAI, No Gemini, etc.).
2. The server runs on an isolated Ubuntu network.
3. All data must be stored locally (Local filesystem or SQLite).

# Core Concept: "Manual AI Simulation"
Since we cannot use real AI generation, the "AI features" (Summary, Audio Overview, Key Topics) will be manually uploaded or inputted by the user. The UI should display them AS IF they were generated, but the backend serves the user-uploaded files.

# Feature Requirements

1. **Dashboard (Home):**
   - List of created "Notebooks".
   - Button to create a new Notebook.

2. **Notebook View (Main Interface):**
   - **Left Sidebar (Sources):**
     - Area to upload source files (PDF, TXT, MD, Images).
     - List of uploaded sources. Clicking a source opens it in a viewer modal or separate panel.
   - **Right/Center Panel (Knowledge Board):**
     - **"Audio Overview" Section:** Instead of generating audio, provide an "Upload Audio" button (for MP3/WAV). Once uploaded, show a sleek audio player similar to NotebookLM's player.
     - **"Saved Responses/Notes" Section:** A chat-like interface. However, instead of a text box sending a prompt to an AI, it acts as a rich-text editor (Markdown support). Users can manually add "Notes," "Summaries," or "Key Takeaways" to share with the team.

3. **File Handling:**
   - Support uploading multiple files per notebook.
   - Simple file storage structure on the Ubuntu server.

# UI/UX Design Requirements
- **Layout:** Three-column or Two-column layout mimicking Google NotebookLM.
  - Left: Source list.
  - Center/Right: Content consumption (Audio player at top, pinned notes/cards below).
- **Styling:** Clean, modern, distinct typography, rounded corners. Use a color palette similar to NotebookLM (Pastel gradients, clean white/gray backgrounds).
- **Responsive:** Must work well on desktop browsers.

# Technical Implementation
- Use **Antigravity** for the frontend and backend logic.
- Ensure the app can be deployed easily on an Ubuntu server (e.g., provide a Dockerfile or a startup script).
- No external CDN links (fonts/icons must be served locally or use standard system fonts).

# Deliverables
1. Complete source code structure.
2. Instructions for running on Ubuntu.
