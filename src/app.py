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
        
        # Store the remaining steps for this session
        all_subtasks = engine.groq.decompose_task(task_text)
        result["all_steps"] = all_subtasks
        result["current_index"] = 0
        result["original_task"] = task_text
        
        print(f"DEBUG: Engine produced: {result}")
        return jsonify(result)
    except Exception as e:
        print(f"DEBUG: EXCEPTION in suggest_task: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/api/feedback", methods=["POST"])
def handle_feedback():
    """Handle user feedback: 'done' or 'too_hard'"""
    print("--- FEEDBACK REQUEST ---")
    try:
        data = request.json
        feedback = data.get("feedback")  # 'done' or 'too_hard'
        current_step = data.get("current_step")
        all_steps = data.get("all_steps", [])
        current_index = data.get("current_index", 0)
        original_task = data.get("original_task", "")
        task_type = data.get("task_type", "general")

        print(f"DEBUG: Feedback={feedback}, Index={current_index}, Step='{current_step}'")

        if feedback == "done":
            # Log success and move to next step
            from db import log_interaction
            log_interaction(task_type, "completed", outcome="success")
            
            next_index = current_index + 1
            if next_index < len(all_steps):
                # Get next step
                next_step = all_steps[next_index]
                size = engine.decide_subtask_size(task_type)
                phrased = engine.groq.phrase_subtask(next_step, size)
                return jsonify({
                    "subtask": phrased,
                    "size": size,
                    "original_subtask": next_step,
                    "all_steps": all_steps,
                    "current_index": next_index,
                    "original_task": original_task,
                    "completed": False
                })
            else:
                # All steps done!
                return jsonify({
                    "subtask": "🎉 Congratulations! You've completed all the steps for this task!",
                    "size": "complete",
                    "completed": True
                })

        elif feedback == "too_hard":
            # Log struggle and break down further
            from db import log_interaction
            log_interaction(task_type, "small", outcome="struggled")
            
            # Ask Groq to break down THIS specific step
            micro_steps = engine.groq.decompose_task(f"Break this into even tinier steps: {current_step}")
            if micro_steps:
                first_micro = micro_steps[0]
                phrased = engine.groq.phrase_subtask(first_micro, "small")
                return jsonify({
                    "subtask": phrased,
                    "size": "small",
                    "original_subtask": first_micro,
                    "all_steps": micro_steps + all_steps[current_index + 1:],  # Replace current with micro + remaining
                    "current_index": 0,
                    "original_task": original_task,
                    "completed": False,
                    "broken_down": True
                })
            else:
                return jsonify({"error": "Could not break down further"}), 500

        return jsonify({"error": "Invalid feedback"}), 400

    except Exception as e:
        print(f"DEBUG: EXCEPTION in feedback: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
