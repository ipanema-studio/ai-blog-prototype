# Role
Act as a Senior Full-Stack Developer proficient in Python and web application frameworks.

# Project Overview
Build a self-hosted web application named "AMS SW Archive".
The goal is to replicate the user interface and user experience of Google's NotebookLM, but strictly for an offline, high-security internal environment.

# Critical Constraints (Security)
1. NO external API calls allowed (No OpenAI, No Gemini, etc.).
2. The server runs on an isolated Ubuntu network.
3. All data must be stored and backed up locally (e.g., SQLite).

# Core Concept: "Manual AI Simulation"
Since we cannot use real AI generation, the "AI features" (Summary, Audio Overview, Key Topics) will be manually uploaded or inputted by the user. The UI should display them AS IF they were generated, but the backend serves the user-uploaded files.

# Feature Requirements

1. **Authentication (Login System):**
   - Implement a login system so that only authorized users can access the site.

2. **Dashboard (Home):**
   - List of created "Notebooks".
   - Button to create a new Notebook.
   - Search bar to search for notebooks by title, author, or keywords.

3. **Notebook View (Main Interface):**
   - **Left Sidebar (Sources):**
     - Area to upload source files (PDF, TXT, MD, Images).
     - List of uploaded sources. Clicking a source opens it in a viewer modal or separate panel.
   - **Center Panel (Overview Section):**
     - Instead of generating overview of the uploaded files, provide an "Edit Overview" button. Once clicked, show a rich-text editor (inserting image support).
   - **Right Panel (Saved Responses/Notes Section):**
     - Area to upload user-created files (PDF, TXT, MD, Images).
     - List of uploaded files. Clicking a file opens it in a viewer modal or separate panel.
     - Users can manually add "Notes," "Summaries," or "Key Takeaways" to share with the team.

4. **File Handling:**
   - Support uploading multiple files per notebook.
   - Simple file storage structure on the Ubuntu server.

# UI/UX Design Requirements
- **Layout:** Three-column layout mimicking Google NotebookLM.
  - Left: Source list.
  - Center/Right: Content consumption.
- **Styling:** Clean, modern, distinct typography, rounded corners. Use a color palette similar to NotebookLM (Pastel gradients, clean white/gray backgrounds).
- **Responsive:** Must work well on desktop browsers.

# Technical Implementation
- Use open-source framework or library for the frontend and backend logic.
- The maintenance of the system should be as simple as possible.
- Ensure the app can be deployed easily on an Ubuntu server.
- No external CDN links (fonts/icons must be served locally).

# Deliverables
1. Complete source code structure.
2. Instructions for running on Ubuntu.
