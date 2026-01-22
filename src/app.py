from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
from dotenv import load_dotenv

# Get the project root directory (one level up from src/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from the correct .env file
dotenv_path = os.path.join(PROJECT_ROOT, '.env')
print(f"DEBUG: Loading .env from: {dotenv_path}")
load_dotenv(dotenv_path)

# Add the current directory to sys.path to ensure local imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db import init_db
from decision_engine import DecisionEngine

# Define static folder as the Vite build output
app = Flask(__name__, static_folder="../frontend/dist")
CORS(app)

# Initialize DB
init_db()

# Initialize Engine
engine = DecisionEngine()

@app.route("/")
def index():
    if os.path.exists(os.path.join(app.static_folder, "index.html")):
        return send_from_directory(app.static_folder, "index.html")
    return "<h1>Backend is running. Frontend build not found.</h1><p>Please run 'npm run build' in the frontend directory.</p>"

@app.route("/<path:path>")
def static_proxy(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
         return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/suggest", methods=["POST"])
def suggest_task():
    print("--- INCOMING REQUEST ---")
    try:
        data = request.json
        print(f"DEBUG: Request Data: {data}")
        task_text = data.get("task_text")
        task_type = data.get("task_type", "general")

        if not task_text:
            print("DEBUG: Task text is missing.")
            return jsonify({"error": "No task provided"}), 400

        print(f"DEBUG: Calling DecisionEngine with: '{task_text}', type='{task_type}'")
        result = engine.get_adaptive_subtask(task_text, task_type)
        print(f"DEBUG: Engine produced: {result}")
        return jsonify(result)
    except Exception as e:
        print(f"DEBUG: EXCEPTION in suggest_task: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
