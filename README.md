# Adaptive Procrastination Agent

## Problem Statement
Procrastination often stems from tasks feeling too big or overwhelming. This agent helps individuals overcome procrastination by breaking tasks down into adaptive, bite-sized micro-tasks based on the user's current context (time of day, past behavior) and task type.

## Agent Contract
1.  **Observation**: The agent observes the task description, task type, and current time of day.
2.  **Reasoning**: It determines the appropriate "task size" (small vs. medium) using a decision engine (e.g., smaller tasks for late evenings).
3.  **Decision**: It decomposes the main task and selects a single, actionable starting point.
4.  **Learning**: It logs interactions to a database to refine future suggestions (e.g., defaulting to smaller tasks after failures).

## Inputs & Outputs
- **Input**: "Write my history essay" (Type: Study)
- **Output**: "Just open your document and write the title and one sentence." (Size: Small)

## Project Structure
- `src/`: Python backend (Flask, SQLite, Decision Engine).
- `frontend/`: React + Tailwind CSS frontend.
- `data/`: SQLite database storage.
- `prompts/`: Text prompts for the LLM.

## Setup & Running

### Prerequisites
- Python 3.10+
- Node.js & npm

### Backend
1. Navigate to the root folder: `adaptive-procrastination-agent`
2. Install Python dependencies: 
   ```bash
   pip install flask flask-cors groq python-dotenv
   ```
3. Run the backend:
   ```bash
   python src/app.py
   ```
   Server runs at `http://localhost:5000`.

### Frontend
1. Navigate to `frontend`: `cd frontend`
2. Install dependencies: `npm install`
3. Run development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at http://localhost:5173.

### Demo
Visit `http://localhost:5173` (Vite default).
Enter a task like "Clean the kitchen" and see the adaptive suggestion.

You can also run the terminal demo:
```bash
python src/demo_agent.py
```
